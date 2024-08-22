---
icon: octicons/project-template-24
search:
  exclude:
tags:
- template
---

# Engine "Overview" Template

This page contains a template for writing the overview of the engine family `X`.

!!! info

    Press the :material-content-copy: button in the code snippet below to copy the
    template and save its content in a new file
    `docs/node_architecture/engines/x_overview.md`.

```html linenums="1" title="docs/node_architecture/engines/x_overview.md"
--- <!-- (1)! -->
icon: octicons/gear-16  <!-- (2)! -->
search:
  exclude: false
categories:
- engine-family <!-- (3)! -->
tags:
- mytag1 <!-- (4)! -->
- engine-overview
---

# X Engine Family <!-- (5)! -->

## Purpose <!-- (6)! -->

Members of the family X do Y and Z, in collaboration with
P, Q, and R, respectively. See [[wikilink-to-X|documentation of X]] <!-- (7)! -->
for background on X, Y and Z.

## Message sequence diagrams <!-- (8)! -->

### [Title of message sequence diagram ⟨𝑖⟩] <!-- (9)! -->

### Forwarding from X to Y <!-- (10)! -->

## Engine Components <!-- (11)! -->

??? note [[X Engine Environment|Engine environment]] <!-- (12)! -->

    <!-- (13)! -->
   --8< "./docs/node_architecture/engines/x_environment.juvix.md"

??? note [[X Engine Dynamics|Engine dynamics]] <!-- (14)! -->

   --8< "./docs/node_architecture/engines/x_dynamics.juvix.md"
```

<!------------------------------------------------------------------------------->

<!-- --8<-- [start:annotations] -->
1. Every Markdown file in the Anoma Specs starts with a YAML front matter block.

2. The icon is a project template icon. Find more icons in the
   [Material
   library](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/?h=icons).

3. The `categories` key is used to categorize the page. In this case, the page is
   categorized as an `engine-family` page.

4. The `tags` key is used to categorize the page. In this case, the page is
   tagged as an `mytag1` page.

5. The heading of the page is the name of the engine family.

6. This section of the page describes in broad terms what the role of (any member of) engine family X is
	- in relation to other [[Engine Instance Type|engine instances]]
    within an Anoma node and/or

	- as part of the whole Anoma instance at large.

	Form

	:   The purpose description is in the form of
        some short paragraphs of prose, possibly just one.

	Conceptual structure

	: One relatively self-contained piece of prose,
	providing links to technical terms and unavoidable jargon.

    Goals

    : An overview/synopsis of the engine family that is
      understandable to a rather wide audience,
      including references to technical terms and unavoidable jargon.

7. Use Wikilinks to link to other pages in the Anoma Specs. The link should be
   in the form `[[wikilink-to-X#anchor|text]]`. The anchor is optional. The
   wikilink is taken from the `nav` section of the `mkdocs.yml` file.

8. This section is **optional** and contains one or several subsections, each of
    which present one message sequence diagram that showcases how members of the
	engine family `X` exchange messages with other engine instances, typically
    from different engine families, but possibly from the same family.[^0]

9.  This section contains a message sequence diagram of engine family X[^01]
    with a title and caption. We can use [`mermaid` sequence
    diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html) to draw
    [message sequence
    diagrams](https://www.uml-diagrams.org/sequence-diagrams.html), using the
    `-)`-syntax by default—expressing that message sending is
    "asynchronous".[^00]

    The goal of this sections is illustrating how a specific instance of a
    collaborative task, data flow, or similar is progressing, message by
    message.


10. The subsection headings allow to reference each of the diagrams if there are
   several ones. Diagrams like the one below.
   <figure markdown="span">

    ```mermaid
    %%{initialize: {'mirrorActors': false} }%%
    sequenceDiagram
        participant Y as Y
        participant E as X
        participant X as X
        X -) E: messageFromX(argOne, argTwo, argThree )
        E -) Y: messageToY(arg, arg')
    ```

   <figcaption markdown="span">

    An X interacting with an X and a Y,
    such that Y is informed about something that has happened at X
    (but without having X's identity revealed).
   </figcaption>
   </figure>

11. This is the final part of the page with includes in the form of **collapsed
    snippets** of the engine components. The engine components are the _environment_
    and the _dynamics_ of the engine family, and _protocol types_, if any.

12. This is a collapsed admonition that links to the `Engine environment` page
    of the engine family. The `[[wikilink-to-X|text]]` syntax is used to link to
    the `Engine environment` page of the engine family.

13. This syntax is used to include the content from the file
    `x_environment.juvix.md`, which must contain the environment definition for
    this engine family.

14. Similarly to the previous point, this is a collapsed admonition that links
    to the `Engine dynamics` page of the engine family. In this case, we expect
    the navigation `nav` section of the `mkdocs.yml` file to contain a link to
    `X Engine Dynamics`.
<!-- --8<-- [end:annotations] -->


## Useful links

- [Use Wiki style links](./../../md/links.md)
- [Include code snippets](./../../md/snippets.md)
- [Mermaid sequence
  diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html)

<!-- footnotes -->

[^0]: The general idea is that each message sequence diagram in the engine
	family page describes a pattern for test cases of any implementation.

[^01]: The subsection headings allow to reference each of the diagrams if there
    are several ones.

[^00]:
    For more on how sequence diagrams naturally arise in actor-like systems,
    consider exploring systems in the
	[stateright explorer](https://www.stateright.rs/seeking-consensus.html#stateright-explorer).

[^000]: Similar goal to [UML use case diagrams](https://www.uml-diagrams.org/use-case-diagrams.html).

