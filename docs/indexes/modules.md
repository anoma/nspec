---
icon: material/keyboard
search:
  exclude: false
tags:
  - index
  - juvix
---

# Modules

All the Juvix modules for the Anoma Specification are listed below.

## Juvix Package version

```
--8<-- "./docs/Package.juvix:package"
```

## Modules by letter

{@@ set juvix_modules_by_letter = get_juvix_modules() @@}
{@@ for letter, juvix_modules in juvix_modules_by_letter.items() @@}
## {@ letter @}
{@@ for entry in juvix_modules @@}

- [{@ entry['qualified_module_name'] @}]({@ entry['url'] @})

{@@ endfor @@}
{@@ endfor @@}
