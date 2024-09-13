---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine-family
- juvix-module
tags:
- mytag1
- engine-dynamics
---

Source code: [[template_dynamics|`./docs/node_architecture/engines/template_dynamics.juvix.md`]]


??? note "Juvix preamble"

    ```juvix
    module node_architecture.engines.template_dynamics;

    import Stdlib.Data.String open;
    import prelude open;
    import node_architecture.basics open;
    import node_architecture.engines.template_overview open;
    import node_architecture.engines.template_environment open;
    import node_architecture.types.engine_family open;
    ```

# `Template` Dynamics

## Overview

This engine does things in the ways described on this page.

## Action labels

??? note "Auxiliary Juvix code"

    <!-- --8<-- [start:auxiliary-juvix-code] -->
    ```juvix
    type SomeActionLabel :=
      | DoThis String
    ;

    type AnotherActionLabel :=
      | DoThat String
    ;
    ```
    <!-- --8<-- [end:auxiliary-juvix-code] -->

<!-- --8<-- [start:template-action-label] -->
```juvix
type TemplateActionLabel :=
  | -- --8<-- [start:TemplateDoAlternative]
    TemplateDoAlternative (Either SomeActionLabel AnotherActionLabel)
    -- --8<-- [end:TemplateDoAlternative]

  | -- --8<-- [start:TemplateDoBoth]
    TemplateDoBoth (Pair SomeActionLabel AnotherActionLabel)
    -- --8<-- [end:TemplateDoBoth]

  | -- --8<-- [start:TemplateDoAnotherAction]
    TemplateDoAnotherAction String
    -- --8<-- [end:TemplateDoAnotherAction]
;
```
<!-- --8<-- [end:template-action-label] -->

### `TemplateDoAlternative`

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:TemplateDoAlternative"

This action label corresponds to performing the `doAlaternative` action
and is relevant for guard `X` and `Y`.

<!-- --8<-- [start:do-alternative-example] -->
```juvix extract-module-statements
module do_alternative_example;
example : TemplateActionLabel :=
  TemplateDoAlternative (prelude.Left (DoThis "do it!"));
end;
```
<!-- --8<-- [end:do-alternative-example] -->

??? quote "`TemplateDoAlternative` action effect"

    #### `Either.Left`

    This alternative does the following.

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state is unchanged as the timer will have all information necessary. |
    | Messages to be sent   | No messages are added to the send queue. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |
    | Acquaintance updates  | None |

    #### `Either.Right`

    This alternative does the following.

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state is unchanged as the timer will have all information necessary. |
    | Messages to be sent   | No messages are added to the send queue. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |
    | Spawned engines       | No engines are spawned by this action. |

### `TemplateDoBoth`

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:TemplateDoBoth"

This action label corresponds to performing both the `doAlternative` and the
`doAnotherAction` action.

??? quote "`TemplateDoBoth` action effect"

    This action consists of two components.

    #### `Pair.fst`

    This alternative does the following.

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state is unchanged as the timer will have all information necessary. |
    | Messages to be sent   | No messages are added to the send queue. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

    #### `Pair.snd`

    This alternative does the following.

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state is unchanged as the timer will have all information necessary. |
    | Messages to be sent   | No messages are added to the send queue. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |

### `TemplateDoAnotherAction`

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:TemplateDoAnotherAction"

This action label corresponds to performing the `doAnotherAction` action.

??? quote "`TemplateDoAnotherAction` action effect"

    This action does the following.

    | Aspect | Description |
    |--------|-------------|
    | State update          | The state is unchanged as the timer will have all information necessary. |
    | Messages to be sent   | No messages are added to the send queue. |
    | Engines to be spawned | No engine is created by this action. |
    | Timer updates         | No timers are set or cancelled. |
    | Spawned engines       | No engines are spawned by this action. |


## Matchable arguments

??? note "Auxiliary Juvix code"

    <!-- --8<-- [start:matchable-arguments-auxiliary-code] -->
    ```juvix
    syntax alias Val := Nat;
    ```
    <!-- --8<-- [end:matchable-arguments-auxiliary-code] -->


<!-- --8<-- [start:template-matchable-argument] -->
```juvix
type TemplateMatchableArgument :=
  | -- --8<-- [start:TemplateMessageOne]
    TemplateMessageOne Val
    -- --8<-- [end:TemplateMessageOne]
  | -- --8<-- [start:TemplateSomeThingFromAMailbox]
    TemplateSomeThingFromAMailbox String
    -- --8<-- [end:TemplateSomeThingFromAMailbox]
;
```
<!-- --8<-- [end:template-matchable-argument] -->

### `TemplateMessageOne`

!!! quote ""

    ```
    --8<-- "./template_dynamics.juvix.md:TemplateMessageOne"
    ```

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

??? example "`TemplateMessageOne` example"

    <!-- --8<-- [start:message-one-example] -->
    ```juvix extract-module-statements
    module message_one_example;
      one : TemplateMatchableArgument := TemplateMessageOne 1;
    end;
    ```
    <!-- --8<-- [end:message-one-example] -->

??? quote "`TemplateMessageOne` matchable argument"

    This matchable argument corresponds to the first message in the list of
    all messages.

    #### `Value1`

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

### `TemplateSomeThingFromAMailbox`

!!! quote ""

    ```
    --8<-- "./template_dynamics.juvix.md:TemplateSomeThingFromAMailbox"
    ```

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

??? example "`TemplateSomeThingFromAMailbox` example"

    <!-- --8<-- [start:some-thing-from-a-mailbox] -->
    ```juvix
    module some_thing_from_a_mailbox;
      someThingFromAMailboxExample : TemplateMatchableArgument :=
        TemplateSomeThingFromAMailbox "Hello World!";
    end;
    ```
    <!-- --8<-- [end:some-thing-from-a-mailbox] -->

??? quote "`TemplateSomeThingFromAMailbox` matchable argument"

    #### `String`

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Precomputation results

??? note "Auxiliary Juvix code"

    <!-- --8<-- [start:pseudo-example-auxiliary-code] -->
    ```juvix
    syntax alias SomeMessageType := Nat;
    ```
    <!-- --8<-- [end:pseudo-example-auxiliary-code] -->

<!-- --8<-- [start:template-precomputation-entry] -->
```juvix
type TemplatePrecomputationEntry :=
  | -- --8<-- [start:TemplateDeleteThisMessageFromMailbox]
    TemplateDeleteThisMessageFromMailbox SomeMessageType Nat
    -- --8<-- [end:TemplateDeleteThisMessageFromMailbox]
  | -- --8<-- [start:TemplateCloseMailbox]
    TemplateCloseMailbox Nat
    -- --8<-- [end:TemplateCloseMailbox]
  ;

TemplatePrecomputation : Type := List TemplatePrecomputationEntry;
```
<!-- --8<-- [end:template-precomputation-entry] -->

Often, the guard detects that we can close a mailbox and that we have to add a
message to a mailbox. Note that we have a list of
`TemplatePrecomputationEntry`-terms as precomputation result and that we
describe the latter in more detail.

### `TemplateDeleteThisMessageFromMailbox`

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:TemplateDeleteThisMessageFromMailbox"

We delete the given message from the mailbox with
the mailbox ID.

<!-- --8<-- [start:TemplateDeleteThisMessageFromMailbox] -->
```juvix extract-module-statements
module template_delete_this_message_from_mailbox;

templateDeleteThisMessageFromMailboxExample : TemplatePrecomputationEntry :=
  TemplateDeleteThisMessageFromMailbox undef 1;
end;
```
<!-- --8<-- [end:TemplateDeleteThisMessageFromMailbox] -->

## Guards

### `TemplateMessageOneGuard`

<figure markdown>

```mermaid
flowchart TD
    C{TemplateMessageOne<br>received?}
    C -->|Yes| D[...]
    C -->|No| E[not enabled]
    D --> F([doAnotherAction n m])
```

<figcaption> TemplateMessageOneGuard flowchart </figcaption>
</figure>

For `TemplateMessageOne`-messages, we do the other action, passing the String
representation of the second and third argument.

<!-- --8<-- [start:message-one-guard] -->
```juvix
-- guard : Type := undef;
messageOneGuard : 
    Maybe Time
    -> Trigger TemplateMsg TemplateTimerHandle
    -> TemplateEnvironment
    -> Maybe (GuardOutput TemplateMatchableArgument TemplateActionLabel TemplatePrecomputation) :=
     \ { _ _ _ :=  just (
      mkGuardOutput@{
        args := [TemplateSomeThingFromAMailbox "Hello World!"]; 
        label := TemplateDoAlternative (Left (DoThis "paramneter 2")); 
        other := [TemplateCloseMailbox 1; TemplateDeleteThisMessageFromMailbox 1337 0]
        }
     )
     };
```
<!-- --8<-- [end:message-one-guard] -->

## Action function

The action function amounts to one single case statement.

??? info "Auxiliary Juvix code"

    ```juvix
    TheActionInput : Type := ActionInput TemplateLocalState TemplateMsg TemplateMailboxState TemplateTimerHandle TemplateMatchableArgument TemplateActionLabel TemplatePrecomputation;
    TheActionOutput : Type := Maybe (ActionEffect TemplateLocalState TemplateMsg TemplateMailboxState TemplateTimerHandle TemplateMatchableArgument TemplateActionLabel TemplatePrecomputation);
    ```

<!-- --8<-- [start:action-function] -->
```juvix
action : TheActionInput -> TheActionInput -> TheActionOutput
  | mkActionInput@{
    guardOutput := out
   } _ := case GuardOutput.label out of {
    | (TemplateDoAlternative (Left _)) := nothing
    | (TemplateDoAlternative (Right _)) := nothing
    | (TemplateDoAnotherAction _) := nothing
    | (TemplateDoBoth (mkPair _ _)) := nothing
    | _ := nothing
}
;
```
<!-- --8<-- [end:action-function] -->

## Engine family summary

<!-- --8<-- [start:template-engine-family] -->
```juvix
TemplateEngineFamily : Type :=
  EngineFamily
  TemplateLocalState
  TemplateMsg
  TemplateMailboxState
  TemplateTimerHandle
  TemplateMatchableArgument
  TemplateActionLabel
  TemplatePrecomputation
;
```
<!-- --8<-- [end:template-engine-family] -->

<!--
### [Action Name ⟨$i$⟩] `{` one such sub-section per guarded action `}`

!!! note

    The description of the actions starts
    with an English language high-level description,
    followed by more detailed descriptions
    of state update, messages to be sent, timers to be set/cancelled/reset,
    and engine instances to be spawned.

    This section may be split into several
    if there are several different cases
    such that each of them deserves a different action label.

### Overview `{` action ⟨𝒊⟩`}`

!!! note

	Some paragraphs of English language prose
	as the author sees fit.

!!! example

	Besides answering the request,
	we have to update the ringbuffer of the mailbox state.

### Code `{` action ⟨$i$⟩ `}`

??? todo "show me the code"

    ♢juvix

### [Action label ⟨$i_j$⟩]

#### Purpose `{`⟨$i_j$⟩`}`

!!! note

    We give quick descriptions of the action for this label.

##### State update `{`⟨$i_j$⟩`}`

!!! note

    Describe the state update

!!! example

    The rate limit is constant in the example.

##### Messages to be sent `{`⟨$i_j$⟩`}`

!!! note

    Describe the messages to be sent
    as a list (or a set if you prefer).

!!! example

    We send only a single message.

    - Send the time stamped hash to the requested »reply to« address.

##### Engines to be created `{`⟨$i_j$⟩`}`

!!! note

    Describe the engines to be created.

!!! example

    No engines are created.

##### Timers to be set/cancelled/reset `{`⟨$i_j$⟩`}`

!!! note

    Describe the engines timers to be set/cancelled/reset.

!!! example

    The time stamping server does not need to set any timers.

## Concurrency, conflict, mutual exclusion. `{` v2' `}`

!!! note "Coming soon™"

    Finally, we need to define the relations of
    concurrency, conflict, mutual exclusion
    between action labels.

-->
