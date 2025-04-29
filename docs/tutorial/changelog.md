---
icon: material/check-all
search:
  exclude: false
  boost: 3
tags:
  - tutorial
  - changelog
---

# Managing the Changelog

We now use `Commitizen` to manage our changelog entries. This simplifies the
process and ensures consistent formatting. The `Commitizen` binary should be
available after installation.

## Adding a New Unreleased Entry

To add a new changelog entry, use the `cz` command provided by `Commitizen`.
This will guide you through the process interactively.

### Using Commitizen

#### Available Types

When prompted, choose one of these types for your commit message:

- `feat` - For new features
- `fix` - For bug fixes
- `docs` - For documentation changes
- `style` - For code style changes (formatting, missing semi-colons, etc.)
- `refactor` - For code changes that neither fix a bug nor add a feature
- `perf` - For performance improvements
- `test` - For adding or correcting tests
- `chore` - For changes to the build process or auxiliary tools

#### Recommended Commit Message Format

For consistency, follow the prompts to:

- Specify the type of change
- Provide a concise description of the change
- Optionally, include the issue number if the change is related to an issue

More information about the command syntax can be found in the [Commitizen
documentation](https://commitizen-tools.github.io/commitizen/tutorials/writing_commits/).
