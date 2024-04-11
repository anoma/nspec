---
icon: material/keyboard
search:
  exclude: false
---

# Juvix Modules

{@@ set juvix_modules_by_letter = get_juvix_modules() @@}
{@@ for letter, juvix_modules in juvix_modules_by_letter.items() @@}
## {@ letter @}
{@@ for entry in juvix_modules @@}

- [{@ entry['module_name'] @}]({@ entry['url'] @})

{@@ endfor @@}
{@@ endfor @@}
