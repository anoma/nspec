---
icon: octicons/project-template-24
search:
  exclude: false
---

# [Engine Family Name] Engine Family

## Purpose

!!! note

	The purpose should describe in broad terms what
	the role of (any member of) engine family [engine family name] is

	- in relation to other engine instances within an Anoma node and/or

	- as part of the whole Anoma instance at large.

	Form

	: The purpose description is in the form of
    some short paragraphs of prose, possibly just one.

	Conceptual Structure

	: One relatively self-contained piece of prose,
	providing links to technical terms and unavoidable jargon.

    Goals

    : Be understandable to a rather wide audience and have all
      the technical terms and jargon linked.


## Message Sequence Diagram

!!! note

    Use one or more message sequence diagrams to show case how
	members of the engine family [engine family name] exchange messages 
    with other engine instances,
	typically from different engine families,
    but possibly from the same family.
	The general idea is that
	each message sequence diagram in the engine family page describes
	a pattern for test cases of any implementation.

	We can use
    [`mermaid` sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html)
    to draw [message sequence diagrams](https://www.uml-diagrams.org/sequence-diagrams.html),
    using the `-)`-syntax by default—expressing that
    message sending is "asynchronous".
	For more on how sequence diagrams naturally arise in actor-like systems,
    consider exploring systems in the
	[stateright explorer](https://www.stateright.rs/seeking-consensus.html#stateright-explorer).

### [Title of Message Sequence Diagram ⟨$i$⟩] `{` several diagrams, $i \in \{1,\dotsc, k\}$ `}`

!!! note

    Form

    : A sequence diagram, by default in mermaid, but better options are welcome.

    Goals

    : Provide at least one example run,
      which amounts to a test case for implementations.
      This goal is similar to that of
      [ᴜᴍʟ use case diagrams](https://www.uml-diagrams.org/use-case-diagrams.html).

!!! tip "on snippeting `--<8--` "

    Snippets do not work with syntax highlighting, yet.
    That is why—for the time being—we
    only provide links to the next two template pages
    (which ideally would just be included here).

### `[[`[Wiki-link] `|` Engine environment`]]` `{` see [[Engine Environment Template]] `}`

### `[[`[Wiki-link] `|` Engine dynamics`]]` `{` see [[Engine Dynamics Template]] `}`
