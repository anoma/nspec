---
icon: material/format-textbox
search:
  exclude: false
tags:
    - guidelines
    - documentation
---

# Tutorials and guidelines for writing Anoma Specification documentation

Our goal is to provide guidelines for writing documentation for the Anoma
Specification. These guidelines help contributors create consistent,
high-quality documents that are easy to read and navigate.

If you want to contribute to this website, ask for access to the
**[anoma/nspec](http://github.com/anoma/nspec)** repository,
and submit a pull request with your changes.

The following tutorials and guidelines are available:

{@@ for dict in nav_dict @@}
{@@ if dict and 'title' in dict and dict.title == "Tutorials for contributors" @@}

{@ dict_to_md(dict.children) @}

{@@ endif @@}
{@@ endfor @@}


{@@ set nav_dict = nav_to_dict(navigation) @@}

{@@ for dict in nav_dict @@}
{@@ if dict and 'title' in dict and dict.title == "Tutorials for contributors" @@}

{@ dict_to_md(dict.children) @}

{@@ endif @@}
{@@ endfor @@}
