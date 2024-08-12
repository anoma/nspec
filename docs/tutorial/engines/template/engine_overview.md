---
icon: octicons/project-template-24
search:
  exclude: false
---

# [Engine Family Name] Engine Family

## Purpose

!!! note "On `Purpose`"

	This section of the page should describe in broad terms what
	the role of (any member of) engine family [engine family name] is

	- in relation to other [[Engine Instance Type|engine instances]]
    within an Anoma node and/or

	- as part of the whole Anoma instance at large.

	Form

	: The purpose description is in the form of
    some short paragraphs of prose, possibly just one.

	Conceptual structure

	: One relatively self-contained piece of prose,
	providing links to technical terms and unavoidable jargon.

    Goals

    : An overview/synopsis of the engine family that is
      understandable to a rather wide audience,
      including references to technical terms and unavoidable jargon.

!!! quote ""

    Members of the family [engine family name]
    do X, Y and Z,
    in collaboration with P, Q, and R, respectively.
    See [documentation of X] for background on X, Y and Z.

## Message sequence diagrams

!!! note "On `Message sequence diagrams`"

    This section contains
    one or more message sequence diagrams to show case how
	members of the engine family [engine family name] exchange messages
    with other engine instances,
	typically from different engine families,
    but possibly from the same family.[^0]

### [Title of message sequence diagram ⟨$i$⟩] `{` several diagrams, $i \in \{1,\dotsc, k\}$ `}`

!!! note "On `[Title of message sequence diagram ⟨$i$⟩]`"

    Each subsection (level three heading) of the
    `Message sequence diagrams` section
    contains a message sequence diagram of
    engine family [engine family name].[^01]

    Form

	: One message sequence diagram with a title and caption.
    We can use
    [`mermaid` sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html)
    to draw [message sequence diagrams](https://www.uml-diagrams.org/sequence-diagrams.html),
    using the `-)`-syntax by default—expressing that
    message sending is "asynchronous".[^00]

    Goal

    : Illustrate how a specific instance of a collaborative task, data flow, or similar is progressing, message by message.

!!! quote ""

    <figure markdown="span">

    ```mermaid
    %%{initialize: {'mirrorActors': false} }%%
    sequenceDiagram
        participant Y as Y
        participant E as [Engine family name]
        participant X as X
        X -) E: messageFromX(argOne, argTwo, argThree )
        E -) Y: messageToY(arg, arg')
    ```

    <figcaption markdown="span">

    An [engine family name] interacting with an X and a Y,
    such that Y is informed about something that has happened at X
    (but without having X's identity revealed).
    </figcaption>
    </figure>

!!! note "Links to the remaining two pages"

    The final part of the page are links to
    the remaining two parts of the engine family specification.[^1]

### `[[`[Wiki-link] `|` Engine environment`]]` `{` see [[Engine Environment Template]] `}`

### `[[`[Wiki-link] `|` Engine dynamics`]]` `{` see [[Engine Dynamics Template]] `}`


<!-- footnotes -->

[^0]: The general idea is that
	each message sequence diagram in the engine family page describes
	a pattern for test cases of any implementation.

[^01]: The subsection headings allow
    to reference each of the diagrams if there are several ones.

[^00]:
    For more on how sequence diagrams naturally arise in actor-like systems,
    consider exploring systems in the
	[stateright explorer](https://www.stateright.rs/seeking-consensus.html#stateright-explorer).

[^000]: The goal is similar to that of
      [ᴜᴍʟ use case diagrams](https://www.uml-diagrams.org/use-case-diagrams.html).


[^1]: Snippets do not work with syntax highlighting, yet.
    That is why—for the time being—we
    only provide links to the next two template pages
    (which ideally would just be included here).
