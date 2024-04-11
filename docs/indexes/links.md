---
icon: material/link
search:
  exclude: false
---

# Quick Links

{@@ set aliases_by_letter = get_aliases() @@}
{@@ for letter, aliases in aliases_by_letter.items() @@}
## {@ letter @}
{@@ for entry in aliases @@}

- [{@ entry['alias'] @}]({@ entry['url'][0] @})

{@@ endfor @@}
{@@ endfor @@}
