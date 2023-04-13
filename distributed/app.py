#!/usr/bin/env python


import argparse
import logging
import os.path
import sys

from distributed.app import create_app

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from lib.anno sandbox.core.startup import drop_privileges

logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
log = logging.getLogger("anno sandbox.distributed")

application = create_app()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("host", nargs="?", default="127.0.0.1", help="Host to listen on.")
    p.add_argument("port", nargs="?", type=int, default=9003, help="Port to listen on.")
    p.add_argument("-u", "--user", type=str, help="Drop user privileges to this user.")
    p.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    args = p.parse_args()

    if args.user:
        drop_privileges(args.user)

    log.setLevel(logging.DEBUG)
    application.run(host=args.host, port=args.port, debug=True)
