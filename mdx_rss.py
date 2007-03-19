import markdown

DEFAULT_URL = "http://www.freewisdom.org/projects/python-markdown/"
DEFAULT_CREATOR = "Yuri Takhteyev"
DEFAULT_TITLE = "Markdown in Python"
GENERATOR = "http://www.freewisdom.org/projects/python-markdown/markdown2rss"

month_map = { "Jan" : "01",
              "Feb" : "02",
              "March" : "03",
              "April" : "04",
              "May" : "05",
              "June" : "06",
              "July" : "07",
              "August" : "08",
              "September" : "09",
              "October" : "10",
              "November" : "11",
              "December" : "12" }

def get_time(heading) :

    heading = heading.split("-")[0]
    heading = heading.strip().replace(",", " ").replace(".", " ")

    month, date, year = heading.split()
    month = month_map[month]

    return rdftime(" ".join((month, date, year, "12:00:00 AM")))

def rdftime(time) :

    time = time.replace(":", " ")
    time = time.replace("/", " ")
    time = time.split()
    return "%s-%s-%sT%s:%s:%s-08:00" % (time[0], time[1], time[2],
                                        time[3], time[4], time[5])


def get_date(text) :
    return "date"

class RssExtension (markdown.Extension):

    def extendMarkdown(self, md, md_globals) :

        self.config = { 'URL' : [DEFAULT_URL, "Main URL"],
                        'CREATOR' : [DEFAULT_CREATOR, "Feed creator's name"],
                        'TITLE' : [DEFAULT_TITLE, "Feed title"] }

        md.xml_mode = True
        
        # Insert a post-processor that would actually add the title tag
        postprocessor = RssPostProcessor(self)
        postprocessor.ext = self
        md.postprocessors.append(postprocessor)
        md.stripTopLevelTags = 0
        md.docType = '<?xml version="1.0" encoding="utf-8"?>\n'

class RssPostProcessor (markdown.Postprocessor):

    def __init__(self, md) :
        
        pass

    def run (self, doc) :

        oldDocElement = doc.documentElement
        rss = doc.createElement("rss")
        rss.setAttribute('version', '2.0')

        doc.appendChild(rss)

        channel = doc.createElement("channel")
        rss.appendChild(channel)
        for tag, text in (("title", self.ext.getConfig("TITLE")),
                          ("link", self.ext.getConfig("URL")),
                          ("description", None)):
            channel.appendChild(doc.createElement(tag, textNode = text))

        for child in oldDocElement.childNodes :

            if child.type == "element" :

                if child.nodeName in ["h1", "h2", "h3", "h4", "h5"] :

                    heading = child.childNodes[0].value.strip()
                    
                    item = doc.createElement("item")
                    channel.appendChild(item)
                    item.appendChild(doc.createElement("link",
                                                       self.ext.getConfig("URL")))

                    item.appendChild(doc.createElement("title", heading))

                    guid = ''.join([x for x in heading if x.isalnum()])

                    guidElem = doc.createElement("guid", guid)
                    guidElem.setAttribute("isPermaLink", "false")
                    item.appendChild(guidElem)

                elif child.nodeName in ["p"] :

                    description = doc.createElement("description")

                    
                    content = "\n".join([node.toxml()
                                         for node in child.childNodes])

                    cdata = doc.createCDATA(content)

                    description.appendChild(cdata)

                    if item :
                        item.appendChild(description)


def makeExtension(configs) :

    return RssExtension(configs)
