# -*- coding: utf-8 -*-
import logging
from logging import DEBUG, INFO, WARN, ERROR, CRITICAL
import sys
import warnings

#
# Exceptions
#

class MarkdownException(Exception):
    """ A Markdown Exception. """
    pass


class MarkdownWarning(Warning):
    """ A Markdown Warning. """
    pass


#
# Global functions
#

def message(level, text):
    """ A wrapper method for logging debug messages. """
    logger =  logging.getLogger('MARKDOWN')
    if logger.handlers:
        # The logger is configured
        logger.log(level, text)
        if level > WARN:
            sys.exit(0)
    elif level > WARN:
        raise MarkdownException, text
    else:
        warnings.warn(text, MarkdownWarning)