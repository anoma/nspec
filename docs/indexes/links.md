---
icon: material/link
---

# Quick Links

{@@ for letter, aliases in aliases_by_letter.items() @@}
## {@ letter @}
{@@ for entry in aliases @@}

- [{@ entry['alias'] @}]({@ entry['url'][0] @})

{@@ endfor @@}
{@@ endfor @@}
