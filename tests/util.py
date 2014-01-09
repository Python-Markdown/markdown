import sys
if sys.version_info[0] == 3:
    from configparser import ConfigParser
else:
    from ConfigParser import SafeConfigParser as ConfigParser

class MarkdownSyntaxError(Exception):
    pass


class CustomConfigParser(ConfigParser):
    def get(self, section, option):
        value = ConfigParser.get(self, section, option)
        if option == 'extensions':
            if len(value.strip()):
                return value.split(',')
            else:
                return []
        if value.lower() in ['yes', 'true', 'on', '1']:
            return True
        if value.lower() in ['no', 'false', 'off', '0']:
            return False
        return value
