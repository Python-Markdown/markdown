title: Video Extension

# Video Extension

**Convert Markdown images pointing to video files into `<video>` HTML elements.**

---

## Installation

The `video` extension is a single Python file.
Enable it like any other Markdown extension:

```python
import markdown

md = markdown.Markdown(extensions=['video'])
```

Or configure it with custom video extensions:

```python
from video import VideoImageExtension

md = markdown.Markdown(
    extensions=[VideoImageExtension(video_extensions=['avi', 'mkv'])]
)
```

---

## Usage

Markdown images with recognized video extensions will be rendered as `<video>` elements:

```markdown
![Intro Video](intro.mp4)
```

Outputs:

```html
<video src="intro.mp4" controls title="Intro Video"></video>
```

* Default attributes: `controls` and `title` (from alt text)
* File extensions recognized by default: `mp4`, `webm`, `ogg`, `mov`

---

## Grav-Style Query Parameters

You can add query parameters in the URL to customize `<video>` attributes:

```markdown
![Looped Video](video.mov?loop=1&autoplay=1&muted=1&controls=0)
```

Outputs:

```html
<video src="video.mov" loop="loop" autoplay="autoplay" muted="muted"></video>
```

| Parameter  | Description                       |
| ---------- | --------------------------------- |
| `autoplay` | Automatically play the video      |
| `loop`     | Loop the video continuously       |
| `muted`    | Mute the video by default         |
| `controls` | Show or hide browser controls     |
| other      | Passed as attributes to `<video>` |

---

## Custom Video Extensions

You can define which file extensions are treated as videos:

```python
md = markdown.Markdown(
    extensions=[VideoImageExtension(video_extensions=['avi', 'mkv'])]
)
```

* Only files with these extensions will be converted to `<video>` elements.
* Other image files will remain `<img>`.

---

## Examples

Markdown:

```markdown
![My Video](demo.webm?autoplay=1&loop=1&muted=1&poster=thumb.png)
```

HTML:

```html
<video src="demo.webm" autoplay="autoplay" loop="loop" muted="muted" poster="thumb.png" controls></video>
```

Markdown image that is not a video:

```markdown
![Image](photo.png)
```

HTML:

```html
<img src="photo.png" alt="Image">
```
