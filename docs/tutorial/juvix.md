---
icon: material/keyboard
tags:
    - Juvix
---


!!! todo

    - [ ] Add example of defining a Juvix module in a page.
    - [ ] Options to skip Juvix preprocessing when building/serving the site.
    - [ ] Add example of how to reference a Juvix module in a page.
    - [ ] Add example of how to reference a Juvix term in a page.
    - [ ] Advice on how to organize Juvix modules in the project.


# Juvix Code

Another feature of the Anoma documentation is the inclusion of Juvix code
throughout its Markdown support. A Juvix Markdown file is a file with extension
`.juvix.md`. These files are preprocesses by the Juvix compiler to generate the
final Markdown file. Only the code blocks with the `juvix` language tag are
processed by the Juvix compiler.

Very important to note is that the first Juvix code block must declare a module
with the name of the file, and each block should be a sequence of well-defined
expressions. This means submodules cannot be split across blocks. The name of
 module must follow the folder structure of the file is in. For example, the
 file `docs/tutorial/basics.juvix.md` must declare the module
`docs.tutorial.basics`.


```markdown
```juvix
module docs.tutorial.basics where
```
```

Refer to the [`everything.juvix.md`](../everything.juvix.md) file located in the `docs` folder to see an example.

!!! tip