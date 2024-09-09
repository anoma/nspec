---
icon: material/keyboard
tags:
    - Juvix
category:
    - tutorial
---

# Render Juvix code

Another feature of the Anoma documentation is the inclusion of Juvix code
throughout its Markdown support. Here we assume you have
[Juvix](https://docs.juvix.org) already installed.

A Juvix Markdown file is a file with extension `.juvix.md`. These files are
preprocesses by the Juvix compiler to generate the final Markdown file. For this
website, we are using `mkdocs-juvix-plugin`.

## Juvix Markdown file structure

Very important to note is that the first Juvix code block must declare a module
with the name of the file, and each block should be a sequence of well-defined
expressions. This means submodules cannot be split across blocks. The name of
 module must follow the folder structure of the file is in. For example, the
 file `tutorial/basics.juvix.md` must declare the module
`tutorial.basics`.

<pre><code>```juvix
module tutorial.basics;
-- ...
```</code></pre>

Refer to the [`everything.juvix.md`](../everything.juvix.md) file located in the
`docs` folder to see an example.

## Hide Juvix code blocks

Juvix code blocks come with a few extra features, such as the ability to hide
the code block from the final output. This is done by adding the `hide`
attribute to the code block. For example:

<pre><code>```juvix hide
module tutorial.basics;
-- ...
```</code></pre>

## Extract inner module statements

Another feature is the ability to extract inner module statements from the code
block. This is done by adding the `extract-module-statements` attribute to the
code block. This option can be accompanied by a number to indicate the number of
statements to extract. For example, the following would only display the content
inside the module `B`, that is, the module `C`.

<pre><code>```juvix extract-module-statements 1
module B;
module C;
-- ...
```</code></pre>

## Snippets of Juvix code

You can also include snippets of Juvix code in your Markdown files. This is done
by adding the `--8<--` comment followed by the path to the file, and optionally
a snippet identifier.

!!! note

    If the path of the file ends with `!`, the raw content of the file
    will be included. Otherwise, for Juvix Markdown files, the content will be
    preprocessed by the Juvix compiler and then the generated HTML will be
    included.


!!! info "Snippet identifier"

    To use a snippet identifier, you must wrap the Juvix code block with the syntax
    `<!-- --8<-- [start:snippet_identifier] -->` and `<!-- --8<-- [end:snippet_identifier] -->`.
    This technique is useful for including specific sections of a file. Alternatively, you
    use the standard `--8<--` markers within the code and extract the snippet by appending a ! at the end of the path.