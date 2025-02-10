---
icon: material/home
description: A work-in-progress specification for the Anoma protocol.
social:
  cards: false
tags:
  - preface
search:
    exclude: true
---

# Preface

<!--ᚦ
    «I have made the single sentence 'This documentation website is a work-in-progress'
    a whole "manifesto" by accident»
-->The Anoma protocol specification is being developed as part of Anoma.
Figuratively speaking,
it is the blueprint of Anoma,
but then, how can the blueprint be part of the whole?
In first approximation,
we are spiraling up,
bootstrapping from what started out as
a write-up of the idea of Anoma for a wider audience
and a prototype implementation loosely based on ... ideas written up.
Less prosaic,
we can make sense of specification as part of the whole
if we consider that
future iterations of the existing code base will be
influenced by the current specification,
and—vice versa—issues discovered while implementing Anoma,
based on the current specs,
provide feed-back for future specifications.
In summary,

> _Anoma, as a whole, is in constant flux._

We fully embrace the dynamic and open nature of Anoma.
We thus offer an unmasked view of
the evolution of the Anoma protocol specification,
also referred to as _Anoma specs,_
the document you are reading right now and here.

We believe that accepting the principle of constant change
is a simple and honest approach to make sure that
there always will be potential for improvement.
To make this work,
we need to cope with the various stages of the evolution.
Thus,
we use [semantic versioning](https://semver.org/) to facilitate meaningful interactions,
be it questions on the forums,
PRs on the github repository,
or other ways of collaboration.

!!! info "Constant improvement in three bullets"

    - Everything in this documentation may be subject to change.
      This is an indispensable prerequisite of Anoma as a system
      to adapt to changes in its environment.<!--ᚦ
      «I should write up a piece on systems of systems»-->

    - The Anoma protocol specification is versioned to keep track of changes.
      Thus,
      if you want to ask a question, add a comment, or suggest improvements,
      it is _indispensable_ to reference the **exact version** of the Anoma specs.
      Please look at the website title or the footer of pages for
      the version of the document—or
      come back here to check whether we have new ways to indicate the version.
      Should you want to reference the frequently changing
      [`main` branch](https://github.com/anoma/nspec),
      please provide a commit hash in place of a version number.

    - The Anoma protocol specification is written in English language.
      However,
      we also embed code snippets,
      written in [juvix](https://juvix.org/).
      The purpose of these code snippets is described [below](#use-of-juvix).
      In short,
      all of Anoma specs should be informative
      without reference to the code.

      !!! note ""

      _Please let us know if the English language descriptions or not precise enough!_

### Purpose and scope

Anoma specs describe the [[Protocol Architecture|protocol architecture]].
In other words,
it provides a blueprint for how components of Anoma protocol instances
may interact to provide functionality.
Thus,
Anoma specs describe what any correct implementation
_has to_ provide and
_may provide._
Anoma specs focus on the rules of the protocol,
not on any particular implementation
(even if we are concurrently working on an [implementation](https://github.com/anoma/anoma)).
How Anoma specs should relate to implementations—in general and in particular—is described
[below](#specification-natural-language-formal-languages-and-beyond).

## Development, evolution, and growth

Besides iterations and improvements of the existing specification,
new components will be added to the Anoma specs.
Roughly,
the table of contents will strictly grow,
not only in depth (detail), but also in length (encompass).
Whether and how ongoing research is to be incorporated into the Anoma specs is
being discussed on the [research forums](https://research.anoma.net/).
This is yet another facet of the principle of
constant evolution of Anoma's concepts and requirements.

## Specification: natural language, formal languages, and beyond

Let us recap what specifications are about, in general—<!--
-->not only about software specifications—<!--
-->to better understand what Anoma specs aim to provide.

!!! quote "Specification [@Nissanke1999]"

    A specification primarily states what is required [for a task],
    providing minimal or no details about how the task should be accomplished.

This goal, i.e., capturing the requirements and essential structure,
can be achieved using English language.
However,
we are sometimes underestimating natural language's flexibility
to change meanings depending on the context,
which can catch us off guard.
We want to avoid any such haphazard ambiguities,
and thus,
in Anoma specs,
we use [formal languages](https://en.wikipedia.org/wiki/Formal_language),
as used and studied by logicians, mathematicians, and computer scientists.

!!! quote "Mathematical expression of specifications"

    A formal specification is, in addition,
    a mathematical expression of what is required (a computational task)
    which may be subjected to mathematical scrutiny (reasoning or proof).

Thus,
the main point of writing formal specification is additional precision,
which is often described as mathematical rigour.[^1]

In summary,
Anoma specs use formal languages to complement natural language
and our list of requests is growing a second element:

- _Please let us know if the English language descriptions or not precise enough!_

- _Please let us know if the formal specification does not match the English language descriptions!_

!!! todo "List and respond to requirements"

    We aim to list and address the functional requirements first, followed by the non-functional requirements.

!!! todo "specs and implementation in detail"

### Mathematical rigour, also for the implementation

At some point in the future,
we may want to make sure that some given implementation matches the protocol,
i.e., demonstrate that an implementation is _correct_;
in short,
we want to _verify_ the implementation.[^2]
There is a large variety of methods,
which often are summarized as _[formal methods](https://en.wikipedia.org/wiki/Formal_methods),_
which we may want to apply, now or in the future.
Note that formal _specification_ is of interest in and of itself:
it forces one to resolve any natural language ambiguities,
and in this way,
we also catch issues that tend to "hide" in natural language.

In summary,
most concepts in the Anoma specs are intended to have formal counterparts
in what we *currently* call _idealized Anoma_ (v0.3-ish).
Anoma specs takes a page out of the proverbial book of formal methods,
but first and foremost,
the purpose of complementing English language prose with Juvix code and formal languages
is mathematical rigour in the Anoma specs.

## Use of Juvix

Throughout the Anoma specs,
we embed code snippets,
written in [Juvix](https://juvix.org/).
While Juvix is still in its infancy,
compared to established languages like Coq,
Isabelle/HOL, Agda or Lean,
it serves our needs surprising well.
Let us highlight some aspects.


- A modern functional programming language with powerful features including
      inductive types, pattern matching, and type classes for expressing
      computational concepts clearly and concisely. For details, see the
      [Essential Juvix](https://docs.juvix.org/0.6.9/tutorials/essential.html)
      tutorial.

- Support for hypertext documentation, including features such as clickable
   references for easy code navigation.

- An easy embedding into Lean4, which we use whenever Juvix's type system restrictions
    call for a more expressive language.

- Built-in support for literate programming, enabling us to seamlessly blend
    type definitions and function definitions with natural language explanations through
    code snippets. This also provides robust type-checking capabilities for all
    code snippets via [Juvix Markdown support](https://docs.juvix.org/),
    ensuring that expressions are well-formed and type-safe.

## Prerequisites

The Anoma specs should  be self-contained, ideally,
but this is rather a promise than a true statement.
For example,
almost certainly there are number technical terms that have become second nature to the authors that should be listed as pre-requisites,
but are not (yet).
Thus,
please reach out,
if you find that we use a term or concept that should at least be referenced
if not recapped in a footnote or note.
In particular,
we want the Anoma specs to grow into a source of information
for at least the following professionals:

- Protocol designers and architects
- Implementation teams
- Verification experts
- External auditors

Eventually, we want to reach the Anoma community at large.
So,
don't hesitate to join the discussion [Anoma](https://research.anoma.net/)!

[^1]: Interestingly, Leslie Lamport goes as far as speaking of "writing math"
    instead of "formally specifying".<!--citation https://duckduckgo.com/?t=ffab&q=lamport+paxos+or+how+to+win+turing+award&iax=videos&ia=videos&iai=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dtw3gsBms-f8#-->

[^2]: Recall that this only makes sense for,
    a specific version of the Anoma specs.