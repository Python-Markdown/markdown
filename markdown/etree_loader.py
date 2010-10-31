from logging import CRITICAL
from md_logging import message
import sys

## Import
def importETree():
    """Import the best implementation of ElementTree, return a module object."""
    etree_in_c = None
    try: # Is it Python 2.5+ with C implemenation of ElementTree installed?
        import xml.etree.cElementTree as etree_in_c
        from xml.etree.ElementTree import Comment
    except ImportError:
        try: # Is it Python 2.5+ with Python implementation of ElementTree?
            import xml.etree.ElementTree as etree
        except ImportError:
            try: # An earlier version of Python with cElementTree installed?
                import cElementTree as etree_in_c
                from elementtree.ElementTree import Comment
            except ImportError:
                try: # An earlier version of Python with Python ElementTree?
                    import elementtree.ElementTree as etree
                except ImportError:
                    message(CRITICAL, "Failed to import ElementTree")
                    sys.exit(1)
    if etree_in_c: 
        if etree_in_c.VERSION < "1.0":
            message(CRITICAL, "cElementTree version 1.0 or higher is required.")
            sys.exit(1)
        # Third party serializers (including ours) test with non-c Comment
        etree_in_c.test_comment = Comment
        return etree_in_c
    elif etree.VERSION < "1.1":
        message(CRITICAL, "ElementTree version 1.1 or higher is required")
        sys.exit(1)
    else:
        return etree

