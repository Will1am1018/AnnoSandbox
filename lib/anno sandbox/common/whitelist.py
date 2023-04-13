
# Copyright (C) 2014-2016 anno sandbox Foundation.
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of anno sandbox Sandbox - 


import os.path

from lib.anno sandbox.common.constants import anno sandbox_ROOT

domains = set()

def is_whitelisted_domain(domain):
    return domain in domains

# Initialize the domain whitelist.
for domain in open(os.path.join(anno sandbox_ROOT, "data", "whitelist", "domain.txt")):
    domains.add(domain.strip())
