#!/usr/bin/env python
"""
   [PlantUML][] Extension for [Python-Markdown][]
   ==============================================

   This plugin implements a block extension which can be used to specify a [PlantUML][] diagram which will be
   converted into an image and inserted in the document.

   Syntax:

      ::uml:: [format="png|svg"] [classes="class1 class2 ..."] [alt="text for alt"]
          PlantUML script diagram
      ::end-uml::

   Example:

      ::uml:: format="png" classes="uml myDiagram" alt="My super diagram"
          Goofy ->  MickeyMouse: calls
          Goofy <-- MickeyMouse: responds
      ::end-uml::

   Options are optional, but if present must be specified in the order format, classes, alt.
   The option value may be enclosed in single or double quotes.

   Installation
   ------------
   You need to install [PlantUML][] (see the site for details) and [Graphviz][] 2.26.3 or later.
   The plugin expects a program `plantuml` in the classpath. If not installed by your package
   manager, you can create a shell script and place it somewhere in the classpath. For example,
   save te following into `/usr/local/bin/plantuml` (supposing [PlantUML][] installed into
   `/opt/plantuml`):

       #!/bin/bash
       java -jar /opt/plantuml/plantuml.jar ${@}

   For [Gentoo Linux][Gentoo] there is an ebuild at http://gpo.zugaina.org/dev-util/plantuml/RDep: you can download
   the ebuild and the `files` subfolder or you can add the `zugaina` repository with [layman][]
   (reccomended).

   [Python-Markdown]: http://pythonhosted.org/Markdown/
   [PlantUML]: http://plantuml.sourceforge.net/
   [Graphviz]: http://www.graphviz.org
   [Gentoo]: http://www.gentoo.org
   [layman]: http://wiki.gentoo.org/wiki/Layman
"""

import os
import re
import tempfile
from subprocess import Popen, PIPE
from zlib import adler32
import logging
import markdown
from markdown.util import etree


logger = logging.getLogger('MARKDOWN')


# For details see https://pythonhosted.org/Markdown/extensions/api.html#blockparser
class PlantUMLBlockProcessor(markdown.blockprocessors.BlockProcessor):
    # Regular expression inspired by the codehilite Markdown plugin
    RE = re.compile(r'''::uml::
                        \s*(format=(?P<quot>"|')(?P<format>\w+)(?P=quot))?
                        \s*(classes=(?P<quot1>"|')(?P<classes>[\w\s]+)(?P=quot1))?
                        \s*(alt=(?P<quot2>"|')(?P<alt>[\w\s"']+)(?P=quot2))?
                    ''', re.VERBOSE)
    # Regular expression for identify end of UML script
    RE_END = re.compile(r'::end-uml::\s*$')

    def test(self, parent, block):
        return self.RE.search(block)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        text = block

        # Parse configuration params
        m = self.RE.search(block)
        format  = m.group('format')  if m.group('format')  else self.config['format']
        classes = m.group('classes') if m.group('classes') else self.config['classes']
        alt     = m.group('alt')     if m.group('alt')     else self.config['alt']

        # Read blocks until end marker found
        while blocks and not self.RE_END.search(block):
            block = blocks.pop(0)
            text += '\n' + block
        else:
            if not blocks:
                raise RuntimeError("UML block not closed")

        # Remove block header and footer
        text = re.sub(self.RE, "", re.sub(self.RE_END, "", text))

        path = os.path.abspath(self.config['outpath'])
        if not os.path.exists(path):
            os.makedirs(path)

        # Generate image from PlantUML script
        imageurl = self.config['siteurl']+self.generate_uml_image(path, text, format)
        # Create image tag and append to the document
        etree.SubElement(parent, "img", src=imageurl, alt=alt, classes=classes)

    def generate_uml_image(self, path, plantuml_code, imgformat):
        tf = tempfile.NamedTemporaryFile(delete=True)
        tf.write('@startuml\n')
        tf.write(plantuml_code.encode('utf8'))
        tf.write('\n@enduml')
        tf.flush()

        if imgformat == 'png':
            imgext = ".png"
            outopt = "-tpng"
        elif imgformat == 'svg':
            imgext = ".svg"
            outopt = "-tsvg"
        else:
            logger.error("Bad uml image format '"+imgformat+"', using png")
            imgext = ".png"
            outopt = "-tpng"

        # make a name
        name = tf.name+imgext
        # build cmd line
        cmdline = [ 'plantuml', '-o', path, outopt, tf.name ]

        try:
            p = Popen(cmdline, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
        except Exception, exc:
            raise Exception('Failed to run plantuml: %s' % exc)
        else:
            if p.returncode == 0:
                # renaming output image using an hash code, just to not pullate
                # output directory with a growing number of images
                name = os.path.join(path, os.path.basename(name))
                newname = os.path.join(path, "%08x" % (adler32(plantuml_code) & 0xffffffff))+imgext

                try:        # for Windows
                    os.remove(newname)
                except Exception:
                    logger.debug('File '+newname+' does not exist, not deleted')

                os.rename(name, newname)
                return 'images/' + os.path.basename(newname)
            else:
                raise RuntimeError('Error in "uml" directive: %s' % err)

# For details see https://pythonhosted.org/Markdown/extensions/api.html#extendmarkdown
class PlantUMLMarkdownExtension(markdown.Extension):
    # For details see https://pythonhosted.org/Markdown/extensions/api.html#configsettings
    def __init__(self, *args, **kwargs):
        self.config = {
            'classes': ["uml","Space separated list of classes for the generated image. Defaults to 'uml'."],
            'alt'    : ["uml diagram", "Text to show when image is not available. Defaults to 'uml diagram'"],
            'format' : ["png", "Format of image to generate (png or svg). Defaults to 'png'."],
            'outpath': ["images", "Directory where to put generated images. Defaults to 'images'."],
            'siteurl': ["", "URL of document, used as a prefix for the image diagram. Defaults to empty string."]
        }

        super(PlantUMLMarkdownExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        blockprocessor = PlantUMLBlockProcessor(md.parser)
        blockprocessor.config = self.getConfigs()
        md.parser.blockprocessors.add('plantuml', blockprocessor, '_begin')

def makeExtension(*args, **kwargs):
    return PlantUMLMarkdownExtension(*args, **kwargs)
