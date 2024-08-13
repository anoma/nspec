---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engine-family
- engine-template
---

# Engine Family and Protocol Types Templates

## Engine family templates

For each engine family,
we have three[^1] different files;
accordingly, we have three different template files.
Each template file comes with an example file,
which can be opened side by side.

1. [[Engine Overview Template]] | [[Ticker Engine Overview | Example]]
2. [[Engine Environment Template]] | [[Ticker Engine Environment | Example]]
3. [[Engine Dynamics Template]] | [[Ticker Engine Dynamics | Example]]

The organisation of these files,
in particular the folder structure,
are explained in the [[Conventions|conventions page]].

## Protocol types template

Finally,
we also have a protocol-level template for types
that are shared among all engine families.

- [[Protocol Types Template]]

## Template syntax and conventions

In the template files,
we shall use text in square brackets to describe generic content.
For example,
`[engine family name]` is a placeholder for the name of
an engine family that is to be described.
Text in pairs of braces,
i.e., `{` and `}`,
are short explanations, comments, or remarks (used only titles).
Occasionally,
we use angled parentheses and italics
for variables,
i.e., _⟨[variableName]⟩;_
for example,
_⟨hash⟩_ is a variable for hashes.
We add footnotes to point out related topics,
give pointers to further reading,
or digress on relevant detail.

Finally,
we use `note` admonitions to describe
what should go into a certain page or (sub-)section.
These `note`s describe the form for each of the (sub-)sections;
typically,
we also describe goals and a conceptual structure.

[^1]: We use different Juvix files
    for "static" and "dynamic" aspects of engine families;
    the "dynamic" aspect rely on the static aspects of _all_ engines.
    In more detail,
    we require definitions of all family-specific message types
    before we can form the type of any message to be sent.
    Finally,
    we have split off the engine overview page,
    which should be a self-contained description of engine families
    in broad terms.
