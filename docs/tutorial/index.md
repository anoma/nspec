---
icon: material/format-textbox
search:
  exclude: false
tags:
    - guidelines
    - documentation
---

# Tutorials and guidelines for writing Anoma Specification documentation

The following tutorials and guidelines are available. If you want to contribute
to this website in anyhow, ask for access to the
**[anoma/nspec](http://github.com/anoma/nspec)** repository, and submit a pull
request with your changes.

{@@ set nav_dict = nav_to_dict(navigation) @@}

{@@ for dict in nav_dict @@}
{@@ if dict and 'title' in dict and dict.title == "Tutorials for contributors" @@}

{@@ for chapter in dict.children @@}
- [[ {@ chapter.title @} ]]
{@@ endfor @@}

{@@ endif @@}
{@@ endfor @@}
