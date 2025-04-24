---
icon: material/check-all
search:
  exclude: false
  boost: 3
tags:
  - tutorial
  - conventions
---

# Run pre-commit checks

Pre-commit hooks are scripts that run before each commit to ensure code quality
by checking for common issues.

## Running pre-commit checks

After installing the development tools, you can, for example, invoke all
checks, by running the following command:

```bash
pre-commit run --all-files
```

Or shorter:

```bash
just check
```
