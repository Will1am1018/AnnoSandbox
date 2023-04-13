
# Originally contributed by Check Point Software Technologies, Ltd.

from lib.common.abstracts import Package
from lib.api.adb import execute_browser

class default_browser(Package):
    """Default Browser analysis package."""
    def __init__(self, options={}):
        super(default_browser, self).__init__(options)

    def start(self, target):
        execute_browser(target)

    def check(self):
        return True

    def finish(self):
        return True
