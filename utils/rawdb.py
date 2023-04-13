#!/usr/bin/env python


import IPython
import os.path
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from lib.anno sandbox.core.database import *

if __name__ == "__main__":
    db = Database(echo=True)
    s = db.Session()

    IPython.start_ipython(user_ns=locals())
