---
icon: material/keyboard
search:
  exclude: false
---

# Modules in Juvix

## Juvix Package version

```
--8<-- "./docs/Package.juvix:package"
```

## Modules by letter

{@@ set juvix_modules_by_letter = get_juvix_modules() @@}
{@@ for letter, juvix_modules in juvix_modules_by_letter.items() @@}
## {@ letter @}
{@@ for entry in juvix_modules @@}

- [{@ entry['module_name'] @}]({@ entry['url'] @})

{@@ endfor @@}
{@@ endfor @@}
