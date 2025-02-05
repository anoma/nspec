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

We use the `unclog` utility to manage our changelog entries. This ensures
consistent formatting and makes it easier to maintain changelog entries.
To install `unclog`, run:

```bash
cargo install unclog
```

## Adding a New Unreleased Entry

There are two ways to add a new changelog entry:

1. Using the CLI directly (recommended)
2. Using your default text editor

### Using the CLI Directly

#### Available Sections

Use one of these sections when adding entries:

- `features` - For new features (**NEW**)
- `changes` - For changes in existing functionality (**CHANGED**)
- `fixes` - For bug fixes (**FIXED**)
- `deprecations` - For soon-to-be removed features (**REMOVED**)

#### Available Subsystems

Use one of the following components for your entry:
- `node`: For changes to the node architecture
- `sys`: For changes to the system architecture
- `spec`: For changes to the general specification
- `types`: For changes to the fundamentals (basic abstractions, types, etc.)
- `apps`: For changes to the applications
- `juvix`: For changes related to the Juvix language/compiler
- `tutorial`: For changes to the tutorial for Spec writers

#### Recommended Call Syntax

For consistency,

- Take into account the number of the pull request
- Use the component that best describes the change
- Use the section that best describes the change
- Add an issue number if the change is related to an issue

The following flags are used:

- `-i` for the entry identifier (filename)
- `-p` for the pull request number
- `-c` for the component (e.g. `node`, `system`, `juvix`, `apps`, `fundamentals`)
- `-s` for the section (e.g. `features`, `fixes`, `deprecations`,:)
- `-m` for the message
- `--editor` for the editor to use (e.g. `nano`, `vim`, `code`)
More information about the command syntax can be found in the [unclog
documentation](https://github.com/informalsystems/unclog).

#### Examples

The following are examples used to populate the changelog for the v0.1.0 release.

- System and Node Architecture

```bash
unclog add -p 210 -i sys210 --editor nano -c sys \
  -s breaking-changes -m "Fix engine message, environment and behavior layout"
```

- Node Architecture

```bash
unclog add -p 179 -i node179 --editor nano -c node \
  -s breaking-changes -m "Reorganize node architecture documentation structure"
```

- Juvix Types and Updates

```bash
unclog add -p 128 -i types128 --editor nano -c types \
  -s features -m "Add new Juvix definitions from PR-84"
```

- Repository Maintenance and

```bash
unclog add -p 135 -i repo135 --editor nano -c repo \
  -s features -m "Show PR number in the site name"
```

- Tutorial and Documentation

```bash
unclog add -p 134 -i tut134 --editor nano -c tutorial \
  -s features -m "Refactor tutorial for wiki-style links"
```

- Application Documentation

```bash
unclog add -p 198 -i apps198 --editor nano -c apps \
  -s features -m "Add transparent RM implementation documentation"
```

- General Specification Changes

```bash
unclog add -p 192 -i spec192 --editor nano -c spec \
  -s breaking-changes -m "Port identity engines to v2 template"
```

- Python-related Changes

```bash
unclog add -p 133 -i py133 --editor nano -c python \
  -s features -m "Add support for multi-line wiki-style links"
```

## Releasing a New Version

1. Update the version number in `docs/Package.juvix` accordingly to the new release:

  ```diff title="docs/Package.juvix"
  module Package;
  ...
  -    version := mkVersion 0 1 1
  +    version := mkVersion 0 1 2;
  ...
  ```

2. Create the release:

  See [[Versioning]] for more details about version numbering.

  ```bash
  unclog release v0.X.Y --editor nano
  ```

  This will:
  - Let you edit the summary of the release
  - Move entries from `.changelog/unreleased/` to a new version section

3. Update the changelog file in the docs directory:

  ```bash
  unclog build > ./docs/changelog.md
  ```

4. Tag the release:

  ```bash
  git tag -a v0.X.Y -m "Release v0.X.Y"
  ```

And push the tag to the repository. The PR corresponding to a release **must**
contain the changelog entries for that release, and a tag.

!!! warning "Do not squash-merge release PRs!"

    Tags associated with individual commits are not preserved when squashing.
