---
icon: octicons/versions-16
tags:
  - GitHub
  - Git
---

# Versioning

The Anoma Specification follows [semantic versioning](https://semver.org/).

```
MAJOR.MINOR.PATCH
```

- MAJOR version when you make incompatible API changes
- MINOR version when you add functionality in a backward compatible manner
- PATCH version when you make backward compatible bug fixes

## Juvix Package version

```
--8<-- "./docs/Package.juvix:package"
```

## More on versioning criteria

- Major version (X.0.0): Incremented for backwards-incompatible changes, like:

    - Breaking changes to core interfaces or types
    - Removal of deprecated functionality
    - Major architectural changes

- Minor version (0.X.0): Incremented for backwards-compatible feature additions:

    - New engines, message types, or behaviours
    - New functionality that doesn't break existing code
    - Deprecation notices for future breaking changes

- Patch version (0.0.X): Incremented for backwards-compatible bug fixes:

    - Documentation improvements
    - Bug fixes that don't change interfaces
    - Minor code clean-up and refactoring



The package started at version 0.1.0 as the initial release.