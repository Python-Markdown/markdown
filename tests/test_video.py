import unittest
import markdown
from video import VideoImageExtension

class TestVideoExtension(unittest.TestCase):
    def make_md(self, **kwargs):
        """Helper to create a Markdown instance with video extension."""
        return markdown.Markdown(extensions=[VideoImageExtension(**kwargs)])

    def test_basic_video(self):
        md = self.make_md()
        src = 'video.mp4'
        html = md.convert(f'![Alt text]({src})')
        self.assertIn('<video', html)
        self.assertIn('src="video.mp4"', html)
        self.assertIn('controls', html)
        self.assertIn('title="Alt text"', html)

    def test_grav_params(self):
        md = self.make_md()
        src = 'video.webm?autoplay=1&loop=1&muted=1&controls=0'
        html = md.convert(f'![test]({src})')
        self.assertIn('<video', html)
        self.assertIn('autoplay="autoplay"', html)
        self.assertIn('loop="loop"', html)
        self.assertIn('muted="muted"', html)
        # Controls explicitly disabled
        self.assertNotIn('controls="controls"', html)

    def test_non_video_image(self):
        md = self.make_md()
        html = md.convert('![img](image.png)')
        # Should remain an <img> element
        self.assertIn('<img', html)
        self.assertNotIn('<video', html)

    def test_custom_extensions(self):
        md = self.make_md(video_extensions=['avi'])
        # avi should convert to video
        html = md.convert('![clip](movie.avi)')
        self.assertIn('<video', html)
        # mp4 should NOT convert because it's not in custom list
        html2 = md.convert('![clip](movie.mp4)')
        self.assertIn('<img', html2)

    def test_other_attributes(self):
        md = self.make_md()
        src = 'video.mp4?poster=thumb.png&preload=auto'
        html = md.convert(f'![v]({src})')
        self.assertIn('poster="thumb.png"', html)
        self.assertIn('preload="auto"', html)


if __name__ == '__main__':
    unittest.main()
