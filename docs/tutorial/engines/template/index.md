---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engine-behaviour
- engine-template
---

# Engine Templates

## Engine templates

For each engine, we have three different files;
accordingly, we mainly have three different template files.
Each template file comes with an example using the Ticker engine,
which can be opened side by side.

1. [[Template Engine]] | [[Ticker Engine]]
2. [[Template Environment]] | [[Ticker Environment]]
3. [[Template Behaviour]] | [[Ticker Behaviour]]

Related to the template files, we have Juvix files defining the types
in the following files:

- [[Engine]]
- [[Engine Environment]]
- [[Engine Behaviour]]

The organisation of these files, in particular the folder structure, are
explained in the [[Engine writing conventions|Folder structure's conventions page]].

!!! info "Template syntax and conventions"

    In the template files, we may use text in square brackets to describe generic
    content. For example, `[engine name]` is a placeholder for the name of an
    engine that is to be described. Text in pairs of braces, i.e., `{` and
    `}`, are short explanations, comments, or remarks (used only in titles).
    Occasionally, we use angled parentheses and italics for variables, i.e.,
    _⟨[variableName]⟩;_ for example, _⟨hash⟩_ is a variable for hashes. We add
    footnotes to point out related topics, give pointers to further reading, or
    digress on relevant detail.

[^1]: We use different Juvix files for "static" and "dynamic" aspects of engine
    families; the "dynamic" aspect rely on the static aspects of _all_ engines.
    In more detail, we require definitions of all engine-specific message types
    before we can form the type of any message to be sent. Finally, we have
    split off the engine overview page, which should be a self-contained
    description of engine families in broad terms.
