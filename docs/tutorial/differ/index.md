---
icon: octicons/file-diff-16
tags:
    - diff
---

# Show Diff

A custom script renders diffs between file versions. The files must reside in
the same directory, named following the pattern `filename-vX.md`, where `X` is a
version number.

For example:

```bash
file_v1.md
file_v2.md
```

The rendered diff is displayed in tabs, with the left tab showing the previous,
and the right tab showing the current version. If no previous version is found,
the left tab is empty. If no current version is found, the right tab is empty.

See [here](./file_v1.md) for an example on how it renders.