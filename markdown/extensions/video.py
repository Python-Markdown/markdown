"""
Video Markdown Extension

Transforms Markdown images pointing to video files into <video> elements,
supporting query parameters for HTML5 attributes.

Usage:
    import markdown
    md = markdown.Markdown(extensions=[
        'video',
        # optional config:
        # ('video', {'video_extensions': ['mp4', 'webm']})
    ])
    html = md.convert('![sample](video.mov?loop=1&controls=0&autoplay=1&muted)')
"""

import os
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as etree
from markdown.inlinepatterns import ImageInlineProcessor
from markdown.extensions import Extension


class VideoImageProcessor(ImageInlineProcessor):
    """Transform images pointing to videos into <video> elements."""

    def __init__(self, pattern, md, video_ext=None):
        super().__init__(pattern, md)
        # allow user-defined extensions; default list
        self.video_ext = tuple(ext.lower().lstrip(".") for ext in (video_ext or ["mp4", "webm", "ogg", "mov"]))

    def handleMatch(self, m, data):
        el, start, end = super().handleMatch(m, data)
        if el is None:
            return None, None, None

        src = el.get("src", "")
        parsed = urlparse(src)
        path, query = parsed.path, parsed.query
        _, ext = os.path.splitext(path.lower())

        if ext.lstrip(".") not in self.video_ext:
            # Not a video; fallback to <img>
            return el, start, end

        # Build <video> element
        video = etree.Element("video")
        video.set("src", src)

        # Parse Grav-style query parameters
        query_params = parse_qs(query, keep_blank_values=True)
        for key, values in query_params.items():
            val = values[0] if values else ""
            # Boolean attributes
            if key.lower() in ("controls", "autoplay", "loop", "muted"):
                if val == "0":
                    continue
                video.set(key, key)
            else:
                # Any other attribute
                video.set(key, val or key)

        # Default controls if not explicitly disabled
        if "controls" not in video.attrib and query_params.get("controls", ["1"])[0] != "0":
            video.set("controls", "controls")

        # Preserve alt text as title
        if el.get("alt"):
            video.set("title", el.get("alt"))

        return video, start, end


class VideoImageExtension(Extension):
    """Markdown extension for video images."""

    def __init__(self, **kwargs):
        self.config = {
            "video_extensions": [
                ["mp4", "webm", "ogg", "mov"],
                "List of allowed video file extensions",
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        pattern = r"\!\["
        md.inlinePatterns.register(
            VideoImageProcessor(pattern, md, self.getConfig("video_extensions")),
            "video_image",
            151,
        )


def makeExtension(**kwargs):
    """Return extension instance."""
    return VideoImageExtension(**kwargs)
