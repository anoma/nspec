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

??? note "Juvix preamble"

    <!-- --8<-- [start:juvix-preamble] -->
    ```juvix
    module tutorial.engines.template.template_dynamics;

    import tutorial.engines.template.template_protocol_types;

    import Stdlib.Data.String open;
    import prelude open;
    ```
    <!-- --8<-- [end:juvix-preamble] -->

# Template Dynamics

## Overview

[...]

## Action labels

??? note "Auxiliary Juvix code"

    <!-- --8<-- [start:auxiliary-juvix-code] -->
    ```juvix
    type someActionLabel :=
      | -- --8<-- [start:doThis]
        doThis String
        -- --8<-- [end:doThis]
    ;
    type anotherActionLabel :=
      | doThat String
    ;
    ```
    <!-- --8<-- [end:auxiliary-juvix-code] -->

<!-- --8<-- [start:template-action-label] -->
```juvix
type TemplateActionLabel :=
  | -- --8<-- [start:doAlternative]
    doAlternative (Either someActionLabel anotherActionLabel)
    -- --8<-- [end:doAlternative]
  | doBoth (Pair someActionLabel anotherActionLabel)
  | doAnotherAction String
;
```
<!-- --8<-- [end:template-action-label] -->

### doAlternative

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:doAlternative"

We perform one of the two altertives,
  depending on user input and randomness—`coming soon™`.

<!-- --8<-- [start:do-alternative-example] -->
```juvix
module do_alternative_example;

doAlternativeExample : TemplateActionLabel :=
  doAlternative (prelude.Left (doThis "do it!"));

end;
```
<!-- --8<-- [end:do-alternative-example] -->

#### Either.Left

The first alternative does _this._

State update

: The state is unchanged as the timer will have all information necessary.

Messages to be sent

: No messages are added to the send queue.

Engines to be spawned

: We shall create a new engine.

Timer updates

: We set a timer for 10 seconds to check up on the spawned engine
  (although that should not be necessary as
    it will send messages as the first thing after spawning).

Acquaintance updates

: None

#### Either.Right

[…]

### doBoth

[…]

### doAnotherAction

[…]

## Matchable arguments

??? note "Auxiliary Juvix code"

    <!-- --8<-- [start:matchable-arguments-auxiliary-code] -->
    ```juvix
    syntax alias thisOneNatFromAllMessages := Nat;
    ```
    <!-- --8<-- [end:matchable-arguments-auxiliary-code] -->

<!-- --8<-- [start:template-matchable-argument] -->
```juvix
type TemplateMatchableArgument :=
  | -- --8<-- [start:messageOne]
    messageOne thisOneNatFromAllMessages
    -- --8<-- [end:messageOne]
  | messageTwo thisOneNatFromAllMessages
  | -- --8<-- [start:someThingFromAMailbox]
    someThingFromAMailbox String
    -- --8<-- [end:someThingFromAMailbox]
;
```
<!-- --8<-- [end:template-matchable-argument] -->

We only match a natural number from messages
and occasionally from a mailbox.

### messageOne

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:messageOne"

We compute a natural number from the arguments of message one.

<!-- --8<-- [start:message-one-example] -->
```juvix
module message_one_example;

messageOneExample : TemplateMatchableArgument := messageOne 1;

end;
```
<!-- --8<-- [end:message-one-example] -->

### messageTwo

[…]

### someThingFromAMailbox

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:someThingFromAMailbox"

We also match a message from a message that
we had stored in a mailbox.
See the section on pre-computation results
for more on how we remember which messages
we will remove from which mailbox.

<!-- --8<-- [start:some-thing-from-a-mailbox] -->
```juvix
module some_thing_from_a_mailbox;
  someThingFromAMailboxExample : TemplateMatchableArgument :=
    someThingFromAMailbox "Hello World!";
end;
```
<!-- --8<-- [end:some-thing-from-a-mailbox] -->

## Precomputation results

??? note "Auxiliary Juvix code"

    <!-- --8<-- [start:pseudo-example-auxiliary-code] -->
    ```juvix
    syntax alias someMessageType := undef;
    ```
    <!-- --8<-- [end:pseudo-example-auxiliary-code] -->

<!-- --8<-- [start:template-precomputation-entry] -->
```juvix
type TemplatePrecomputationEntry :=
  | -- --8<-- [start:deleteThisMessageFromMailbox]
    deleteThisMessageFromMailbox someMessageType Nat
    -- --8<-- [end:deleteThisMessageFromMailbox]
  | closeMailbox Nat
;

TemplatePrecomputation : Type := List TemplatePrecomputationEntry;
```
<!-- --8<-- [end:template-precomputation-entry] -->

Often, the guard detects that we can close a mailbox
and that we have to add a message to a mailbox.
Note that we have a list of `TemplatePrecomputationEntry`-terms
as precomputation result
and that we describe the latter in more detail.

### deleteThisMessageFromMailbox

!!! quote ""

    --8<-- "./template_dynamics.juvix.md:deleteThisMessageFromMailbox"

We delete the given message from the mailbox with
the mailbox ID.

<!-- --8<-- [start:delete-this-message-from-mailbox] -->
```juvix
module delete_this_message_from_mailbox;

deleteThisMessageFromMailboxExample : TemplatePrecomputationEntry :=
  deleteThisMessageFromMailbox undef 1;
end;
```
<!-- --8<-- [end:delete-this-message-from-mailbox] -->

## Guards

### messageOneGuard

```mermaid
flowchart TD
    C{messageOne<br>received?}
    C -->|Yes| D[enabled<br>n := argTwo<br>m := argThree ]
    C -->|No| E[not enabled]
    D --> F([doAnotherAction n m])
```

For `messageOne`-messages,
we do the other action,
passing the String representation
of the second and third argument.

<!-- --8<-- [start:message-one-guard] -->
```juvix
--- messageOneGuard (see todo)
guard : Type := undef;
```
<!-- --8<-- [end:message-one-guard] -->

!!! todo "fix/add code (with conversion from Nat to String)"

    ```
    messageOneGuard :  Maybe Time
        -> Trigger I H
            -> EngineEnvironment S I M H
                -> Maybe (GuardOutput A L X) :=
                […] ;
    ```

## Action dependencies and conflict resolution

We just use the lexicographical ordering.

!!! todo "fix code"

<!-- --8<-- [start:lexicographical-ordering] -->
```juvix
lexicographicalOrdering : Type -> Type := undef;
```
<!-- --8<-- [end:lexicographical-ordering] -->

## Action function

The action function amounts to one single
case statement.

!!! todo "fix code"

<!-- --8<-- [start:action-function] -->
```juvix
actionFunction : Type -> Type := undef;
```
<!-- --8<-- [end:action-function] -->

## Engine family summary

!!! todo "fix example 👇 (undef!)"

<!-- --8<-- [start:template-engine-family] -->
```juvix
TemplateEngineFamily : Type := undef;
```
<!-- --8<-- [end:template-engine-family] -->

!!! todo "fix example 👇 (undef!)"

<!-- --8<-- [start:template-engine-family-example] -->
```juvix
module template_engine_family;
templateEngineFamilyExample : TemplateEngineFamily := undef;
end;
```
<!-- --8<-- [end:template-engine-family-example] -->

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

??? note "show me the code"

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