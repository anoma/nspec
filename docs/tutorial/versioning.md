---
icon: octicons/versions-16
tags:
  - tutorial
  - conventions
  - versioning
---

# Versioning

The Anoma Specification follows [semantic versioning](https://semver.org/).

```
MAJOR.MINOR.PATCH
```

- MAJOR version when you make incompatible API changes
- MINOR version when you add functionality in a backward compatible manner
- PATCH version when you make backward compatible bug fixes

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

## Preparing a new version

- [ ] Update `mkdocs.yml`
- [ ] Update `docs/Package.juvix`
- [ ] Update `docs/references/ref.bib`
- [ ] Make sure to run `just sync` to update the dependencies and `just build` to check that the code is still typechecking.
- [ ] Git tag the new version
- [ ] Release a new changelog entry

### Update `mkdocs.yml`

Update the `site_version` to the new version.

```diff title="mkdocs.yml"
- site_version: !ENV [SITE_VERSION, "v0.1.0"]
+ site_version: !ENV [SITE_VERSION, "v0.1.1"]
```

### Update `nspec` Juvix package version

```diff title="docs/Package.juvix"
package : Package :=
  defaultPackage@{
    name := "nspec";
-    version := mkVersion 0 1 0;
+    version := mkVersion 0 1 1;
    dependencies :=
      [github "anoma" "juvix-stdlib" "v0.6.0"; github "anoma" "juvix-containers" "v0.14.1"]
  };
```

### Update `docs/ref.bib`

Update the version of the `nspec` package in the `ref.bib` file.

```diff title="docs/ref.bib"
@software{nspec,
  author = {Anoma},
  title = {Anoma Specification},
-  version = {0.1.0},
+  version = {0.1.1},
  url = {https://github.com/anoma/nspec}
}
```

## Update `VERSION`

```diff title="VERSION"
-0.1.0
+0.1.1
```

## Update `pyproject.toml`

```diff title="pyproject.toml"
- version = "0.1.0"
+ version = "0.1.1"
```


### Git tag the new version

```bash
git tag v0.1.1
```

### Release a new changelog entry

Follow the [[Updating the changelog#releasing-a-new-version]] tutorial for more information on how to
release a new changelog entry. This tutorial uses `unclog` to create a new changelog entry.

The package started at version 0.1.0 as the initial release.
