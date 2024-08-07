---
icon: octicons/project-template-24
search:
  exclude: false
---

# [Engine Family Name] Engine Family

## Purpose

!!! note

	The purpose should describe in broad terms what
	the role of (any member of) this engine family is

	- in relation to other engine instances within an Anoma node and/or

	- as part of the whole Anoma instance at large.
	

	Form
	
	: The purpose description is in the form of some short paragraphs of prose, possibly just one.

	Conceptual Structure
	
	: One relatively self-contained piece of prose,
	providing links to techincal terms and unavoidable jargon.


## Message Sequence Diagram `{`optional`}`

!!! note

	We can use one or more message sequence diagrams to show how
	members of the engine family exchange messages with other engine instances,
	typically from different engine families.
	The general idea is that
	each message sequence diagram in the engine family page describes
	a pattern for test cases.
	We can use
    [`mermaid` sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html) 
    to draw [message sequence diagrams](https://www.uml-diagrams.org/sequence-diagrams.html),
    using the `-)`-syntax by default,
    expressing that message sending is "asynchronous".
	For more on how
    actor systems (or models of them) give rise to sequence diagrams,
    consider exploring systems using
	[stateright](https://www.stateright.rs/)'s [state explorer](https://www.stateright.rs/seeking-consensus.html#stateright-explorer).


### [Title of Message Sequence Diagram 1]


!!! note 


    Form
    
    : A mermaid or other message sequence diagram.

### `[[`[Wikilink] `|` Engine Environment`]]` 

### `[[`[Wikilink] `|` Engine Dynamics`]]`

