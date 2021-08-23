try:
  import lxml.etree as etree
except:
  import xml.etree.ElementTree as etree
  
def __getattr__(name):
    """Get attribute."""
    
    return getattr(etree, name)
