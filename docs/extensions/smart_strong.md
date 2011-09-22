Smart_Strong
------------

Summary

The Markdown Smart_Strong Extension adds smarter handling of double underscores
within words. This does for double underscores what 'smart_emphasis' does for 
single underscores.

The Smart_Strong Extension is included in the standard Markdown library.

Usage
-----

    >>> import markdown
    >>> markdown.markdown('Text with double__underscore__words.', \
                          extensions=['smart_strong'])
    u'<p>Text with double__underscore__words.</p>'
    >>> markdown.markdown('__Strong__ still works.', \
                          extensions=['smart_strong'])
    u'<p><strong>Strong</strong> still works.</p>'
    >>> markdown.markdown('__this__works__too__.', \
                          extensions=['smart_strong'])
    u'<p><strong>this__works__too</strong>.</p>'

This extension is also included with the [Extra](extra.html) Extension. You may
call that extension to get this behavior with all the other features of 'Extra'.

    >>> markdown.markdown(text, extensions=['extra'])

