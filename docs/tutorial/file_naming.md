---
icon: octicons/typography-16
search:
  exclude: false
  boost: 3
tags:
  - tutorial
  - conventions
---


# `snake_case` convention for naming files and folders

The Anoma Specification uses the `snake_case` convention for naming files and
folders.

## Guidelines

- Use lowercase letters.
- Separate words with underscores `_`, instead of dashes `-` or camel case.
- No special characters or spaces.

## Pros

- Readability: Improves readability by clearly separating words in names, making
  code more understandable.
- Consistency: Creates a uniform naming style throughout the codebase.
- Compatibility: Widely supported across different programming languages and
  platforms, no issues with case sensitivity.

## Cons

- Length: Can make names longer.
- Visual Clutter: The underscores can create visual clutter, especially in
  longer names. We suffer from this, specially in engine's description files.


!!! info

    If you find any file or folder that does not follow this convention, please
    create an issue or a pull request to fix it. Thank you for your help!
