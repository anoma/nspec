# Engine Family Templates

For each engine template,
we have three different files
and accordingly, we have three[^1] different template files,
each of which comes with an example file, which can be opened side by side.

1. [[Engine Overview]] ([[Ticker Engine Overview | Engine Overview Example]])
2. [[Engine Environment]] ([[Ticker Engine Environment | Engine Environment Example]])
3. [[Engine Dynamics]] ([[Ticker Engine Dynamics | Engine Dynamics Example]])

In the template files,
we shall use text in square brackets to describe generic content.
For example,
`[Engine Family Name]` is a placeholder for the name of
an engine family that is to be described.
Text in pairs of braces `{` and `}` are short explanations
and comments (used only titles).
Occasionally,
we use angled parentheses and italics
for variables _⟨[variableName]⟩,_
e.g, _⟨hash⟩_ is a variable for hashes.
Finally,
we use `note` admonitions to describe
what should go into a certain section;
this will become clear if you
look at a template an its example side by side.

[^1]: The reason we split up the files is
    the need for several different Juvix files
    for different data.
    In particular,
    we need to have definitions for all engine-specific message types
    before we can form the type of any message to be sent
    (in the dynamics section).


