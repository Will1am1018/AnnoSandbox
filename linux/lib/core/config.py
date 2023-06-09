

import ConfigParser

class Config:
    def __init__(self, cfg):
        """@param cfg: configuration file."""
        config = ConfigParser.ConfigParser(allow_no_value=True)
        config.read(cfg)

        for section in config.sections():
            for name, raw_value in config.items(section):
                if name == "file_name":
                    value = config.get(section, name)
                else:
                    try:
                        value = config.getboolean(section, name)
                    except ValueError:
                        try:
                            value = config.getint(section, name)
                        except ValueError:
                            value = config.get(section, name)
                setattr(self, name, value)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default

    def get_options(self):
        """Get analysis options.
        @return: options dict.
        """
        # The analysis package can be provided with some options in the
        # following format:
        #   option1=value1,option2=value2,option3=value3
        #
        # Here we parse such options and provide a dictionary that will be made
        # accessible to the analysis package.
        options = {}
        if hasattr(self, "options"):
            try:
                # Split the options by comma.
                fields = self.options.split(",")
            except ValueError as e:
                pass
            else:
                for field in fields:
                    # Split the name and the value of the option.
                    try:
                        key, value = field.split("=", 1)
                    except ValueError:
                        pass
                    else:
                        # If the parsing went good, we add the option to the
                        # dictionary.
                        options[key.strip()] = value.strip()

        return options
