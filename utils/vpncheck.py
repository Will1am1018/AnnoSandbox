#!/usr/bin/env python
# Copyright (C) 2016 anno sandbox Foundation.
# This file is part of anno sandbox Sandbox - 


import argparse
import fcntl
import os
import socket
import struct
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from lib.anno sandbox.core.rooter import rooter, vpns
from lib.anno sandbox.core.startup import init_rooter, init_routing

SIOCGIFADDR = 0x8915

def get_ip_address(interface):
    """Retrieves the local IP address of a network interface."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buf = fcntl.ioctl(s.fileno(), SIOCGIFADDR, struct.pack("256s", interface))
    return socket.inet_ntoa(buf[20:24])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server", nargs="?", default="/tmp/anno sandbox-rooter", help="Unix socket path of the server")
    parser.add_argument("client", nargs="?", default="/tmp/anno sandbox-vpncheck", help="Unix socket path of this client")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    if os.path.exists(args.client):
        os.unlink(args.client)

    init_rooter()
    init_routing()

    error = 0
    for vpn, status in rooter("vpn_status").items():
        if vpn not in vpns:
            print "Not a configured VPN", vpn
            continue

        if not rooter("nic_available", vpns[vpn].interface):
            print>>sys.stderr, "VPN is no longer available", vpn
            error = 1
            continue

        ipaddr = get_ip_address(vpns[vpn].interface)

        rooter("forward_enable", vpns[vpn].interface, vpns[vpn].interface, ipaddr)
        rooter("srcroute_enable", vpns[vpn].rt_table, ipaddr)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.bind((ipaddr, 0))
            sock.connect(("myip.anno sandbox.sh", 80))
            sock.send("GET / HTTP/1.0\r\nHost: myip.anno sandbox.sh\r\n\r\n")
            ret = sock.recv(4096).split("\r\n\r\n", 1)[-1]

            if args.verbose:
                print vpns[vpn].name, ipaddr, ret
        except socket.error:
            print>>sys.stderr, "Unable to connect through VPN", vpn
            error = 1

        rooter("forward_disable", vpns[vpn].interface, vpns[vpn].interface, ipaddr)
        rooter("srcroute_disable", vpns[vpn].rt_table, ipaddr)

    exit(error)
