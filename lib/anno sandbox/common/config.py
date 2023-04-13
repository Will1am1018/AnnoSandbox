
# Copyright (C) 2014-2016 anno sandbox Foundation.
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of anno sandbox Sandbox - 


import os
import ConfigParser

from lib.anno sandbox.common.constants import anno sandbox_ROOT
from lib.anno sandbox.common.exceptions import anno sandboxOperationalError
from lib.anno sandbox.common.objects import Dictionary

class Config():
    """Configuration file parser.

    :param file_name: file name without extension.
    :param cfg: configuration file path.
    """

    def __init__(self, file_name="anno sandbox", cfg=None):
        """
        :param file_name: file name without extension.
        :param cfg: configuration file path.
        """
        config = ConfigParser.ConfigParser()

        if cfg:
            config.read(cfg)
        else:
            config.read(os.path.join(anno sandbox_ROOT, "conf", "%s.conf" % file_name))

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name, raw_value in config.items(section):
                try:
                    # Ugly fix to avoid '0' and '1' to be parsed as a
                    # boolean value.
                    # We raise an exception to goto fail^w parse it
                    # as integer.
                    if config.get(section, name) in ["0", "1"]:
                        raise ValueError

                    value = config.getboolean(section, name)
                except ValueError:
                    try:
                        value = config.getint(section, name)
                    except ValueError:
                        value = config.get(section, name)

                setattr(getattr(self, section), name, value)

    def get(self, section):
        """Get option.

        :param section: section to fetch.
        :raise anno sandboxOperationalError: if section not found.
        :return: option value.
        """
        try:
            return getattr(self, section)
        except AttributeError as e:
            raise anno sandboxOperationalError("Option %s is not found in "
                                         "configuration, error: %s" %
                                         (section, e))

def parse_options(options):
    """Parse the analysis options field to a dictionary."""
    ret = {}
    for field in options.split(","):
        if "=" not in field:
            continue

        key, value = field.split("=", 1)
        ret[key.strip()] = value.strip()
    return ret

def emit_options(options):
    """Emit the analysis options from a dictionary to a string."""
    return ",".join("%s=%s" % (k, v) for k, v in options.items())
