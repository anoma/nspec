---
icon: material/alert-circle-outline
---

# Disclaimer

This documentation website is a work-in-progress [**formal specification**](#formal-specification-approach) of the
Anoma protocol. We refer to this documentation as the "Anoma specs".
It is important to understand what this documentation is and what it is not.

---

### General information

- Everything in this documentation is subject to change.

- The documentation is versioned, so refer to the specific version when
    discussing this documentation. Where is the version? Latest is not the
    version, we use semver. Find the version in website title or the footer of the page.

- This documentation is written in English, natural language in combination with
    mathematical notation and Juvix code snippets (read more about it
    [below](#use-of-juvix)).

---

### Purpose and scope

Anoma specs outline the [[Protocol Architecture|protocol architecture]],
providing a blueprint for the protocol and its components. It does **not
include**:

- The operating system Anoma says it will be, as this is not yet fully sketched.
- The implementation, which is currently under development.
- A prototype, since there is no working implementation at this stage.

Anoma specs are intended to guide implementers rather than serve as an
implementation themselves. The focus is on what the protocol does, not on how it
should be implemented. Implementation details are left to the discretion of the
[Anoma engineering team](https://github.com/anoma/anoma). This is related to the
purpose of [any formal specification](#formal-specification-approach).

---

### Development and Evolution

Some aspects of the Anoma system related to the protocol are not yet specified
and will be added as they are developed. This is due to the ongoing evolution of
Anoma's concept and its requirements. Follow the [research
forum](https://research.anoma.net/) for more information.

---

## Formal specification approach

We adhere to the principles of formal specification:

!!! quote "Formal specification"

    A specification primarily states what is required, providing minimal or no details about how the task should be accomplished. Additionally, a formal specification includes a mathematical expression of these requirements, allowing for mathematical scrutiny. [@Nissanke1999]

!!! todo "List and respond to requirements"

    We aim to list and address the functional requirements first, followed by the non-functional requirements.

---

### Formal specification is not formal verification

We want to verify the protocol and demonstrate its correctness at some point.
However, this documentation does not constitute a formal verification of the
protocol; therefore, proofs or proof-like structures are not meant to be
included. Formal verification is another project.

Most constructs in this documentation are intended to have formal descriptions,
usage statements, constraints, or properties. Therefore, although we do not 
include a proof rigorous specification, this website suggests what should be
verified.

---

## Use of Juvix

Throughout this documentation, you will find code snippets written in
[Juvix](https://juvix.org/). This choice is deliberate for several reasons:

- It is our in-house programming language for building Anoma applications,
   providing natural alignment with the ecosystem. More users of the language
   the better.

- Although Juvix is still maturing compared to established languages like Coq,
    Isabelle/HOL, Agda or Lean, and while not specifically designed as a formal
    specification language, it serves our needs exceptionally well by providing:

    - A modern functional programming language with powerful features including
      inductive types, pattern matching, and type classes for expressing
      computational concepts clearly and concisely. For details, see the
      [Essential Juvix](https://docs.juvix.org/0.6.9/tutorials/essential.html)
      tutorial.

    - Built-in support for literate programming, enabling us to seamlessly blend
      precise mathematical notation with natural language explanations through
      documented code snippets. This is, robust type-checking capabilities for all
      code snippets via [Juvix Markdown support](https://docs.juvix.org/),
      ensuring that expressions are well-formed and type-safe (subject to compiler
      correctness).

    - Support for HTML-like documentation with features like clickable
      references for easy code navigation.
      
- The implementation of Anoma, separated from the specification, is written in
    Elixir, another programming language that follows the same principles of
    functional programming that Juvix does.

---

## Intended audience

The primary purpose of this specification is to facilitate clear communication
between Anoma engineers and researchers. This documentation is a product of the
*specs-team*, part of the [Anoma Research](https://research.anoma.net/) team.

Although the specification is intended for Anoma engineers and researchers, it
can also prove useful to:

- Protocol designers and architects.
- Implementation teams.
- Verification specialists.
- External auditors.
- The broader Anoma community.

