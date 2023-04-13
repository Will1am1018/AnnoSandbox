#!/bin/sh
set -e

echo "### NOTICE ###" >&2
echo "This script is a work-in-progress, has not been yet documented, " >&2
echo "and may not work as expected." >&2
echo "### END OF NOTICE ###" >&2

# TODO Load Virtual Machines into tmpfs, if enabled.

_about_upstart() {
    echo "Using Upstart technique.."
}

_install_configuration() {
    if [ -f "/etc/default/anno sandbox" ]; then
        # TODO Ask yes/no to force overwrite.
        echo "Not overwriting existing configuration.."
        return
    fi

    cat > /etc/default/anno sandbox << EOF
# Configuration file for the anno sandbox Sandbox service(s).

# It is possible to allow the virtual machines to connect to the entire
# internet through the vmcloak-iptables script. Enable by uncommenting and
# setting the following value. Give the network interface(s) that can allow
# internet access to the virtual machines.
# VMINTERNET="eth0 wlan0"

# IP address and port of the anno sandbox API. anno sandbox API is by default
# turned *OFF*. Enable by uncommenting and setting the value.
# APIADDR="127.0.0.1"
# APIPORT=8090

# IP address and port of the anno sandbox Web Interface. The anno sandbox Web Interface
# is by default turned *OFF*. Enable by uncommenting and setting the value.
# WEBADDR="127.0.0.1"
# WEBPORT=8000

# Run Suricata in the background?
SURICATA="0"

# Start anno sandbox in verbose mode. Toggle to 1 to enable verbose mode.
VERBOSE="0"
EOF
}

_remove_configuration() {
    rm -f /etc/default/anno sandbox
}

_install_upstart() {
    cat > /etc/init/anno sandbox.conf << EOF
# anno sandbox daemon service.

description "anno sandbox daemon"
start on runlevel [2345]
chdir "$anno sandbox"

# Give anno sandbox time to cleanup.
kill signal SIGINT
kill timeout 600

# Restart anno sandbox if it exits.
respawn

# Upstart ignores limits found in /etc/security/limits.conf.
limit nofile 499999 999999

env CONFFILE="$CONFFILE"
env VMINTERNET=""
env CHECKVMS="/etc/default/anno sandbox-setup"

pre-start script
    . "\$CONFFILE"

    vmcloak-vboxnet0

    if [ -n "\$VMINTERNET" ]; then
        vmcloak-iptables 192.168.56.1/24 "\$VMINTERNET"
    fi

    # Check up on all VMs and fix any if required.
    if [ -f "\$CHECKVMS" ]; then
        ./utils/setup.sh -S "\$CHECKVMS" -V
    fi
end script

script
    . "\$CONFFILE"

    if [ "\$VERBOSE" -eq 0 ]; then
        exec ./anno sandbox.py -u "$USERNAME"
    else
        exec ./anno sandbox.py -u "$USERNAME" -d
    fi
end script
EOF

    cat > /etc/init/anno sandbox-process.conf << EOF
# anno sandbox results processing service.

description "start anno sandbox results processing"
start on started anno sandbox
stop on stopped anno sandbox

env PROCESSES=4

pre-start script
    echo STARTING
    for i in \$(seq 1 \$PROCESSES); do
        start anno sandbox-process2 INSTANCE=process\$i
    done
end script
EOF

    cat > /etc/init/anno sandbox-process2.conf << EOF
# anno sandbox results processing service.

description "anno sandbox results processing"
stop on stopping anno sandbox-process
setuid "$USERNAME"
chdir "$anno sandbox"
instance \$INSTANCE

# Restart anno sandbox report processing if it exits unexpectedly.
respawn

env CONFFILE="$CONFFILE"

script
    . "\$CONFFILE"

    exec ./utils/process2.py "\$INSTANCE"
end script
EOF

    cat > /etc/init/anno sandbox-api.conf << EOF
# anno sandbox API server service.

description "anno sandbox api server"
start on started anno sandbox
stop on stopped anno sandbox
setuid "$USERNAME"
chdir "$anno sandbox"

env CONFFILE="$CONFFILE"
env APIADDR=""
env APIPORT=8090

script
    . "\$CONFFILE"

    if [ -n "\$APIADDR" ]; then
        exec ./utils/api.py -H "\$APIADDR" -p "\$APIPORT"
    fi
end script
EOF

    cat > /etc/init/anno sandbox-distributed-instance.conf << EOF
# anno sandbox distributed API node instance service.

description "anno sandbox distributed api node instance service"
setuid "$USERNAME"
chdir "$anno sandbox/distributed"
instance \$INSTANCE
respawn

env CONFFILE="$CONFFILE"

script
    . "\$CONFFILE"

    if [ "\$VERBOSE" -eq 0 ]; then
        exec ./instance.py "\$INSTANCE"
    else
        exec ./instance.py "\$INSTANCE" -v
    fi
end script
EOF

    cat > /etc/uwsgi/apps-available/anno sandbox-distributed.ini << EOF
[uwsgi]
plugins = python
chdir = $anno sandbox/distributed
file = app.py
uid = $USERNAME
gid = $USERNAME
EOF

    ln -s /etc/uwsgi/apps-available/anno sandbox-distributed.ini \
        /etc/uwsgi/apps-enabled/anno sandbox-distributed.ini

    cat > /etc/nginx/sites-available/anno sandbox-distributed << EOF
upstream _uwsgi_anno sandbox_distributed {
    server unix:/run/uwsgi/app/anno sandbox-distributed/socket;
}

server {
    # If required, prepend a listening IP address.
    listen 9003;

    location / {
        client_max_body_size 100M;
        uwsgi_pass _uwsgi_anno sandbox_distributed;
        include uwsgi_params;
    }
}
EOF

    ln -s /etc/nginx/sites-available/anno sandbox-distributed \
        /etc/nginx/sites-enabled/anno sandbox-distributed

    cat > /etc/init/anno sandbox-web.conf << EOF
# anno sandbox Web Interface server.

description "anno sandbox web interface service"
start on started anno sandbox
stop on stopped anno sandbox
setuid "$USERNAME"
chdir "$(readlink -f "$anno sandbox/web/")"

env CONFFILE="$CONFFILE"
env WEBADDR=""
env WEBPORT=8000

script
    . "\$CONFFILE"

    if [ -n "\$WEBADDR" ]; then
        exec ./manage.py runserver "\$WEBADDR:\$WEBPORT"
    fi
end script
EOF
    echo "anno sandbox Service scripts installed!"
}

_remove_upstart() {
    rm -f /etc/init/anno sandbox.conf
    rm -f /etc/init/anno sandbox-api.conf
    rm -f /etc/init/anno sandbox-process.conf
    rm -f /etc/init/anno sandbox-process2.conf
    rm -f /etc/init/anno sandbox-distributed-instance.conf
    rm -f /etc/init/anno sandbox-web.conf
}

_reload_upstart() {
    initctl reload-configuration
}

_start_upstart() {
    initctl start anno sandbox
}

_stop_upstart() {
    initctl stop anno sandbox
}

_restart_upstart() {
    initctl restart anno sandbox
}

case "$(lsb_release -is)" in
    Ubuntu)
        alias _about=_about_upstart
        alias _install=_install_upstart
        alias _remove=_remove_upstart
        alias _reload=_reload_upstart
        alias _start=_start_upstart
        alias _stop=_stop_upstart
        alias _restart=_restart_upstart
        ;;

    *)
        echo "Unsupported Linux distribution.."
        exit 1
esac

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <install|remove|start|stop>"
    echo "-u --username: Username from which to run anno sandbox."
    echo "-c --anno sandbox:   Directory where anno sandbox is located."
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    echo "This script should be run as root."
    exit 1
fi

USERNAME="anno sandbox"
CONFFILE="/etc/default/anno sandbox"
anno sandbox="/home/anno sandbox/anno sandbox/"

# Note that this way the variables have to be set before the
# actions are invoked.
while [ "$#" -ne 0 ]; do
    ACTION="$1"
    shift

    case "$ACTION" in
        install)
            _about
            _install
            _install_configuration
            _reload
            ;;

        remove)
            _remove
            _remove_configuration
            _reload
            ;;

        start)
            _start
            ;;

        stop)
            _stop
            ;;

        restart)
            _restart
            ;;

        -u|--username)
            USERNAME="$1"
            shift
            ;;

        -c|--anno sandbox)
            anno sandbox="$1"
            shift
            ;;

        *)
            echo "Requested invalid action."
            exit 1
    esac
done
