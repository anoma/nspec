---
icon: material/image
search:
  exclude: false
todos: False
---

## Including Images

Images should be stored in the `docs/images` folder.


### Basic Image Syntax

To add an image, apply the following syntax:

```markdown
![Alt Text](logo.svg){: width="200"}
```

#### Displayed Image Example

The syntax above will render the image in your document like so:

![Alt Text](logo.svg){: width="200"}

!!! tip "Enhanced Image Display"

    Use an HTML `<figure>` element with a `<figcaption>` for a refined presentation with captions. Markdown can also be used within the caption:

    ```html
    <figure markdown="1">
      <img src="docs/images/image-name.png" alt="Alt Text">
      <figcaption markdown="span">Image caption text can include *Markdown*!</figcaption>
    </figure>
    ```
