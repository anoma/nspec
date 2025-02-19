---
icon: material/image
search:
  exclude: false
tags:
  - tutorial
  - conventions
todos: False
---

# Support for including images

Images should be stored in the `docs/images` folder.
Use the [[File Naming Conventions]] also for naming images.

!!! warning "Image handling in Markdown"

    Use standard Markdown image syntax (`![Alt text](image.png)`) rather than HTML image tags.
    HTML image tags are not processed by MkDocs, are not validated, and may not work as expected.
    In particular, their `src` attribute is not processed by our image processing script.

## Syntax

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

      ![Alt Text](image-name.png)

      <figcaption markdown="span">Image caption text can include *Markdown*!</figcaption>
    </figure>
    ```
