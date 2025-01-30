---
icon: material/check-all
search:
  exclude: false
  boost: 3
tags:
  - tutorial
  - git
---

# Run pre-commit checks

Pre-commit hooks are scripts that run before each commit to ensure code quality by checking for common issues.

## Running pre-commit checks

If you have the Python environment ready, you can, for example, invoke all
checks, by running the following command:

```bash
pre-commit run --all-files
```

## Customizing hooks

No satisfied with the checks, customize hooks by editing `.pre-commit-config.yaml`. Refer to [pre-commit
documentation](https://pre-commit.com/) for more details.