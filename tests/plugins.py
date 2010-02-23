import traceback
from util import MarkdownSyntaxError
from nose.plugins import Plugin
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin

class Markdown(ErrorClassPlugin):
    """ Add MarkdownSyntaxError and ensure proper formatting. """
    mdsyntax = ErrorClass(MarkdownSyntaxError, 
                          label='MarkdownSyntaxError', 
                          isfailure=True)
    enabled = True

    def configure(self, options, conf):
        self.conf = conf

    def addError(self, test, err):
        """ Ensure other plugins see the error by returning nothing here. """
        pass

    def formatError(self, test, err):
        """ Remove unnessecary and unhelpful traceback from error report. """
        et, ev, tb = err
        if et.__name__ == 'MarkdownSyntaxError':
            return et, ev, ''
        return err


def escape(html):
    """ Escape HTML for display as source within HTML. """
    html = html.replace('&', '&amp;')
    html = html.replace('<', '&lt;')
    html = html.replace('>', '&gt;')
    return html


class HtmlOutput(Plugin):
    """Output test results as ugly, unstyled html. """
    
    name = 'html-output'
    score = 2 # run late
    enabled = True
    
    def __init__(self):
        super(HtmlOutput, self).__init__()
        self.html = [ '<html><head>',
                      '<title>Test output</title>',
                      '</head><body>' ]
   
    def configure(self, options, conf):
        self.conf = conf

    def addSuccess(self, test):
        self.html.append('<span>ok</span>')
    
    def addError(self, test, err):
        err = self.formatErr(err)
        self.html.append('<span>ERROR</span>')
        self.html.append('<pre>%s</pre>' % escape(err))
            
    def addFailure(self, test, err):
        err = self.formatErr(err)
        self.html.append('<span>FAIL</span>')
        self.html.append('<pre>%s</pre>' % escape(err))

    def finalize(self, result):
        self.html.append('<div>')
        self.html.append("Ran %d test%s" %
                         (result.testsRun, result.testsRun != 1 and "s" 
or ""))
        self.html.append('</div>')
        self.html.append('<div>')
        if not result.wasSuccessful():
            self.html.extend(['<span>FAILED (',
                              'failures=%d ' % len(result.failures),
                              'errors=%d' % len(result.errors)])
            for cls in result.errorClasses.keys():
                storage, label, isfail = result.errorClasses[cls]
                if len(storage):
                    self.html.append(' %ss=%d' % (label, len(storage)))
            self.html.append(')</span>')
        else:
            self.html.append('OK')
        self.html.append('</div></body></html>')
        f = open('test-output.html', 'w')
        for l in self.html:
            f.write(l)
        f.close()

    def formatErr(self, err):
        exctype, value, tb = err
        return ''.join(traceback.format_exception(exctype, value, tb))
    
    def startContext(self, ctx):
        try:
            n = ctx.__name__
        except AttributeError:
            n = str(ctx).replace('<', '').replace('>', '')
        self.html.extend(['<fieldset>', '<legend>', n, '</legend>'])
        try:
            path = ctx.__file__.replace('.pyc', '.py')
            self.html.extend(['<div>', path, '</div>'])
        except AttributeError:
            pass

    def stopContext(self, ctx):
        self.html.append('</fieldset>')
    
    def startTest(self, test):
        self.html.extend([ '<div><span>',
                           test.shortDescription() or str(test),
                           '</span>' ])
        
    def stopTest(self, test):
        self.html.append('</div>')

