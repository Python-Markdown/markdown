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
        if value.lower() in ['yes', 'true', 'on']:
            return True
        if value.lower() in ['no', 'false', 'off']:
            return False
        return value
