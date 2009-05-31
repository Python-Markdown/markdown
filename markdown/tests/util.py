from ConfigParser import SafeConfigParser

class MdSyntaxError(Exception):
    pass


class CustomConfigParser(SafeConfigParser):
    def get(self, section, option):
        value = SafeConfigParser.get(self, section, option)
        if option == 'extensions':
            if len(value.strip()):
                return value.split(',')
            else:
                return []
        return value
