# Copyright (C) 2017-2018 anno sandbox Foundation.
# This file is part of anno sandbox Sandbox - 


import ctypes
import os.path
import platform
import shutil
import _winreg

from lib.common.defines import NTDLL, UNICODE_STRING
from lib.common.exceptions import anno sandboxError
from lib.common.registry import set_regkey, del_regkey

class Driver(object):
    def __init__(self, driver_name, install_name):
        self.driver_name = driver_name
        self.install_name = install_name
        self.is_64bit = platform.machine().endswith("64")

    def install(self):
        self.copy_driver()
        self.set_regkey(
            "ImagePath", _winreg.REG_SZ,
            "\\SystemRoot\\system32\\drivers\\%s.sys" % self.install_name
        )
        self.set_regkey("Start", _winreg.REG_DWORD, 3)
        self.set_regkey("Type", _winreg.REG_DWORD, 1)
        self.set_regkey("ErrorControl", _winreg.REG_DWORD, 1)
        self.load_driver()
        self.del_regkeys()

    def copy_driver(self):
        if platform.machine().endswith("64"):
            self.driver_path = os.path.join(
                "bin", "%s-x64.sys" % self.driver_name
            )
            install_dir = os.path.expandvars(
                "%SystemRoot%\\sysnative\\drivers"
            )
        else:
            self.driver_path = os.path.join(
                "bin", "%s-x86.sys" % self.driver_name
            )
            install_dir = os.path.expandvars(
                "%SystemRoot%\\system32\\drivers"
            )

        if not os.path.exists(self.driver_path):
            raise anno sandboxError("Error locating %s driver!" % self.driver_name)

        self.install_path = os.path.join(
            install_dir, "%s.sys" % self.install_name
        )

        shutil.copy(self.driver_path, self.install_path)

    def set_regkey(self, key, type_, value):
        set_regkey(
            _winreg.HKEY_LOCAL_MACHINE,
            "SYSTEM\\CurrentControlSet\\Services\\%s" % self.install_name,
            key, type_, value
        )

    def del_regkeys(self):
        regkeys = [
            "SYSTEM\\CurrentControlSet\\Services\\%s\\Enum",
            "SYSTEM\\CurrentControlSet\\Services\\%s\\Security",
            "SYSTEM\\CurrentControlSet\\Services\\%s",
        ]

        for regkey in regkeys:
            del_regkey(_winreg.HKEY_LOCAL_MACHINE, regkey % self.install_name)

    def load_driver(self):
        regkey = (
            u"\\Registry\\Machine\\System"
            u"\\CurrentControlSet\\Services\\%s" % self.install_name
        )
        us = UNICODE_STRING()
        us.Buffer = regkey
        us.Length = len(regkey) * 2
        us.MaximumLength = us.Length

        status = NTDLL.NtLoadDriver(ctypes.byref(us)) % 2**32
        if status == 0xc0000428:
            raise anno sandboxError(
                "Driver Signature Enforcement has not been disabled."
            )
        if status:
            raise anno sandboxError(
                "Unable to load the %s driver: 0x%x" %
                (self.driver_name, status)
            )
