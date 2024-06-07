---
icon: material/keyboard
tags:
    - Juvix
---



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
 file `tutorial/basics.juvix.md` must declare the module
`tutorial.basics`.

<pre><code>```juvix
module tutorial.basics;
-- ...
```</code></pre>


Refer to the [`everything.juvix.md`](../everything.juvix.md) file located in the
`docs` folder to see an example.

Juvix code blocks come with a few extra features, such as the ability to hide
the code block from the final output. This is done by adding the `hide`
attribute to the code block. For example:

<pre><code>```juvix hide
module tutorial.basics;
-- ...
```</code></pre>

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



!!! tip