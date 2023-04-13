

import os
import tempfile
from lib.common.utils import random_string

ROOT = os.path.join(tempfile.gettempdir(), random_string(6, 10))

PATHS = {"root"   : ROOT,
         "logs"   : os.path.join(ROOT, "logs"),
         "files"  : os.path.join(ROOT, "files"),
         "shots"  : os.path.join(ROOT, "shots"),
         "memory" : os.path.join(ROOT, "memory"),
         "drop"   : os.path.join(ROOT, "drop")}
