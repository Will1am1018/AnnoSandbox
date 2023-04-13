#!/bin/sh

# Install Suricata.
# $ sudo apt-get install software-properties-common
# $ sudo add-apt-repository ppa:oisf/suricata-stable
# $ sudo apt-get update
# $ sudo apt-get install suricata
#
# Setup Suricata configuration.
#
# In /etc/default/suricata, set RUN to "no".
#
# In /etc/suricata/suricata.yaml apply the following changes;
# * Set "unix-command.enabled" to "yes".
# * Set "unix-command.filename" to "anno sandbox.socket".
# * Set "outputs.eve-log.enabled" to "yes".
# * Set "run-as.user to "your anno sandbox user"
# * Set "run-as.group to "your anno sandbox user group"
# * TODO More items.
#
# Add "@reboot /opt/anno sandbox/utils/suricata.sh" to the root crontab.

. /etc/default/anno sandbox

# Do we want to run Suricata in the background?
if [ "$SURICATA" -eq 0 ]; then
    exit
fi

mkdir /var/run/suricata
chown anno sandbox:anno sandbox /var/run/suricata

suricata --unix-socket -D

while [ ! -e /var/run/suricata/anno sandbox.socket ]; do
    sleep 1
done
