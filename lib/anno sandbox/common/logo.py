
# Copyright (C) 2014-2016 anno sandbox Foundation.
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of anno sandbox Sandbox - 


import sys
import random

from lib.anno sandbox.common.colors import color, yellow
from lib.anno sandbox.common.constants import anno sandbox_VERSION

def logo():
    """
    Anno Sandbox asciiarts.

    :return: asciiarts array.
    """
    logos = []

    logos.append("""
     ____        _     _       _____     _                 
    | __ )  ___ | | __| |     |  ___|_ _| | ___ ___  _ __  
    |  _ \ / _ \| |/ _` |_____| |_ / _` | |/ __/ _ \| '_ \ 
    | |_) | (_) | | (_| |_____|  _| (_| | | (_| (_) | | | |
    |____/ \___/|_|\__,_|     |_|  \__,_|_|\___\___/|_| |_|
    """)


    print(color(random.choice(logos), random.randrange(31, 37)))
    print
    print(" Anno Sandbox Sandbox %s" % yellow(anno sandbox_VERSION))
    print(" www.Anno Sandbox.org")
    print(" Copyright (c) 2021-2023")
    print
    sys.stdout.flush()
