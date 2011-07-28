from ConfigParser import SafeConfigParser

class MarkdownSyntaxError(Exception):
    pass


class CustomConfigParser(SafeConfigParser):
    def get(self, section, option):
        value = SafeConfigParser.get(self, section, option)
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
