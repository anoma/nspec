---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- signs_for
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.signs_for_messages open public;
    import arch.node.engines.signs_for_environment open public;
    import arch.node.engines.signs_for_behaviour open public;
    open signs_for_environment_example;
    ```

# SignsFor Engine

The Signs For Engine manages `signs_for` relationships between identities. A `signs_for` relationship indicates that one identity can produce signatures (commitments) on behalf of another identity.

## Purpose

The Signs For Engine maintains and manages the state of `signs_for` relationships between identities. It handles queries about these relationships, allows submission of new evidence, and provides information about existing relationships. This is useful in scenarios where signature delegation or proxy signing is required.

## Components

- [[SignsFor Messages]]
- [[SignsFor Environment]]
- [[SignsFor Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:SignsForEngine] -->
```juvix
SignsForEngine : Type := Engine
  SignsForLocalState
  SignsForMailboxState
  SignsForTimerHandle
  SignsForMatchableArgument
  SignsForActionLabel
  SignsForPrecomputation;
```
<!-- --8<-- [end:SignsForEngine] -->

### Example of a signsFor engine

```juvix extract-module-statements
exampleSignsForEngine : SignsForEngine := mkEngine@{
    node := Curve25519PubKey "0xabcd1234";
    name := "signsFor";
    behaviour := signsForBehaviour;
    initEnv := signsForEnvironmentExample;
  };
```

where `signsForEnvironmentExample` is defined as follows:

--8<-- "./signs_for_environment.juvix.md:environment-example"
