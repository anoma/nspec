---
icon: octicons/project-template-24
search:
  exclude: false
---

??? note "Juvix preamble: ʜᴇʀᴇ 👇 are the `module` declaration, `import`s, `open`s, etc."

    ```juvix
    module tutorial.engines.template.engine_dynamics;

    import tutorial.engines.template.template_protocol_types;

    import Stdlib.Data.String open;
    import prelude open;
    ```

# [Engine Family Name] Dynamics

!!! note

    In this page,
    we define a set of
    [[Engine Family Types#guards|guards]]
    and an
    [[Engine Family Types#action-function|action function]]
    to complete the definition of the
    engine family [engine family name].
    Most notably,
    this involves the definition of
    action labels
    and the associated actions that the engine can perform.

    ??? note "Short summary of guards and the action function"

        In short,
        the action function computes the effects of actions to be taken,
        while being a [pure function](https://en.wikipedia.org/wiki/Pure_function);
        <!--(see also [[On LTS semantics of guarded actions]]);-->
        the guards determine for each possible circumstance
        which actions are to performed as a reaction.

    Conceptual structure

    :   First, we want a description of all action labels,
    in particular the effects of the associated actions;
    we also want a description of how
    conflicts of sets of action labels are resolved
    (unless we have a "smooth" engine with no such conflicts).[^1]
    After action labels and their conflict resoultion
    have been described,
    we come to the description of guards,
    which, in turn,
    requires that we define the type of
    matched arguments and pre-computation results beforehand.
    Finally,
    the page contains the code of the action function,
    including code comments;
    however,
    the most ímportant points should be described in markdown.[^2']

    Form

    : The form is prescribed by this template file.

    Goal

    : The main goals are two:

    : - an overview of the action lables and guards which should be accessible
        to a widest possible audience that is understandable
        after reading the engine environment page up to
        the end of the message type section;

    : - a documentation of details
        that are relevant for any implementation
        (other than the model implementation).

    !!! warning "This is really ɪᴍᴘᴏʀᴛᴀɴᴛ!"

        The data of any action label should be
        as independent as possible of the engine environment.
        Roughly,
        replacing one eninge implementation with a different one
        that uses a "completely different" environment type
        should always be possible.[^2]

        🚨 **Never** use the local state type of environments
        for arguments of the action label. 🚨

        Whenever you consider doing this ☝️,
        the relevant data _must_ be moved
        to the precomputation result;
        also note that the action function
        has access to the _whole environment!_
<!--ᚦ leave this here for the time being¶
    This involves the definition of three types—or type parameters,
    to be precise—besides those defined in the engine environment,
    whose terms guards compute and
    also feature in the input of the action function.

    Matched arguments

    :   Matched arguments are typically obtained by pattern matching of messages,
        be it from a trigger or previously received messages in one of the mailboxes.
        
    Action labels

    :   Action labels describe actions that members of the engine family
        [engine family name] can perform, in principle.


    Precomputation results

    :   Guards may involve non-trivial computations,
        wich should not be repeated;
         instead the results are passed on as precomputation result.

--><!--
    For this,
    we first define a datatype of _action labels,_
    each of which defines an action that
    a member of the engine family can perform
    (in response to messages or timer notifications)—without
    mentioning the specific circumastances that call
    for performing the action that the action label describes.
    The action labels are complemented by a set of guarded actions,
    which describe situations under which certain actions are actually performed.-->

!!! todo "definition of _engine system_"

    Where do we have the definition of engine system now?

## Overview

!!! note "On `Overview`"

    Form

    : The overview is free form,
    but preferably short
    (as many descriptions will follow).

## Action labels

!!! note "On `Action labels`" 

    We first define a Juvix type of action labels.
    This type has to be a record type or algebraic data type
    for the purposes of the Anoma specification.
    The constructors of this type are called _action tags,_
    in analogy to _message tag._

    ??? note "Action labels determine unique action effects: _∀ label ∃! effect_"

        The action label alone has to determine
        the ensuing action effect,
        i.e.,
        how the state is to be updated,
        which list of messages has to be added to the send queue,
        what set of engines to be spawned,
        the changes to the timer list of the engine environment.
        Note that the action tag may take parameters.

        👉 _The action tag parameters should be "minimal"!_

        Thus,
        for each parameter that you may consider to add to an action label,
        consider to move it to the type of
        [[Engine Dynamics Template#matchable-arguments|matchable arguments]]
        or arbitrary
        [[Engine Dynamics Template#precomputation-results|precomputation results]].

    Conceptual structure

    : Each action tag should have a small
    description of what the effects of the associated action are,
    in broad terms.

    Form

    :   We first give the Juvix definition of
        the message label datatype
        named `[EngineFamilyName]ActionLabel`.
        Then we have 
        one level three heading `### [Action Tag ⟨i⟩]`
        for each action tag of the Juvix datatype.
        Each of those sub-subections, in turn,
        has
 
        `#### [Action Tag ⟨i⟩]` level four heading

        :   We first have the code snippet of the constructor,
            quoting the resepective portion of the Juvix datatype.
            Then,
            we have a description in broad terms of the associated action.
            The action may be structured,
            for example there may
            be alternatives or sequences of "sub-actions".
            If the action has non-trivial structure,
            the structure of this sub-subsection should reflect
            the structure of the action.[^3]
            _There should be not be any case distinctions,
            as case distinctions should be covered by guards._
            The description should end with a definition list
            that explains each of the arguments of the action tag.
            Finally,
            we give an example of an action lable term.

            `##### [Action Tag ⟨i⟩] state update` 

            :   Describe the state update.


            `##### [Action Tag ⟨i⟩] messages to be sent` 

            :   Describe messages to be sent.

            `##### [Action Tag ⟨i⟩] engines to be spawned` 

            :   Describe engines to be spawned. 

            `##### [Action Tag ⟨i⟩] timer updates` 

            :   Describe timer updates.

    Goal

    : An understanding of the purpose of the actions that action labels describe,
    without the need to consult later sections.

    !!! quote "Pseudo-example"
    
        !!! todo "adapt the peudo-example to match the template"
        
        Consider the following code.
    
        ```juvix
        type someActionLabel :=
          | doThis String
          ;
        type anotherActionLabel :=
          | doThat String
        ;
    
        type allLabels :=
          | doAlternative (Either someActionLabel anotherActionLabel)
          | doBoth (Pair someActionLabel anotherActionLabel)
          | doAnotherAction String
        ;
        ```
    
        The corresponding structure would be the one of the last type.
    
        ### doAlternative
    
        We do one of the two.
    
        #### Either.Left `{` optional `}`
    
        The first alternative does _this._
    
        #### Either.Right  `{` optional `}`
    
        The other alternative does _that._
    
        ### doBoth
    
        Here we do both.
    
        #### first  `{` optional `}`
    
        Well, we have described _this_ above.
    
        #### second  `{` optional `}`
    
        Well, we have described _that_ above.
    
        ### doAnotherAction
    
        Finally, we have a third kind of action
        that also has to be documented.

## Matchable arguments 

!!! note "On `Matchable arguments`"

    Matchable arguments are inspired by pattern matching;
    e.g., in
    [`receive do`-statements](https://hexdocs.pm/elixir/main/processes.html#sending-and-receiving-messages)
    in Elixir,
    we may match a subset of the arguments of a message tag.
    The type of matchable arguments defines
    which arguments possibly will be matched.
    Note that some ímportant arguments may already be covered by
    the arguments of the action label.

    Form

    : A Juvix algebraic datatype followed by documentation.

    Goal

    : Get an overview of which arguments we want to pass to the action function
      besides the action label.


## Precomputation results

!!! note "On `Precomputation results`"

    Guard evaluation may involve non-trivial computation
    that should not have to be repeated in
    the computation of the actions effects.
    Thus,
    we have a third input for action functions,
    which is meant to relay any precomputation results
    beyond matching and label computation.

    Form

    : A type definition with an explanation of its purpose.

    Goal

    : Get an overview of non-trivial computations performed by guards.


!!! warning "Execution time may be unbounded (in V2)"

    New events are "muted" for the time of
    guard evaluation and action execution.
    The only envisaged way around this is
    the specification of a "hard" maximum duration of action processing,
    after which the action processing is terminated with a timeout,
    and a previously specified default value is returned
    (typically also indicating the occurrence of the timeout).
    However,
    this is not part of V2 specs.

## Guards


!!! note "On `Guards`"

    For each guard of the engine family,
    we provide a guard description.

### [Guard ⟨guard $i$⟩] `{` $0 < i < l$ `}`

!!! note "On `[Guard ⟨guard $i$⟩]`" 

    For each guard
    we want a short description
    of which actions are enable under which conditions.

    Conceptual structure

    : We essentially need a decision tree, flow chart, or similar for

    - how to determine whether this guard enables actions and then which ones

    - describe the action label, matched arguments,
    and pre-computations results for each of the cases;
    for the latter,
    we may describe how or when they are computed along the way.

    Form

    : There are three parts:

    1. a [flowchart](https://en.wikipedia.org/wiki/Flowchart)
    that illustrates the guard logic.
    Recall that decision nodes are diamond shaped (`{ decision node text }`);
    we (ab-)use rectangular boxes to describe matching of arguments
    or other computations
    (`[ processing node text ]`)
    and the final guard output
    is summarized in terminal nodes
    (`([matched arguments,  action label, precompuation result])`),
    which Mermaid calls "stadiums".

    2. Juvix code of the actual guard function

    3. an English language description of the code in broad terms.

    Goal

    : The flowchart should illustrate at a glance
    how actions are enabled by this guard.
    

!!! warning

    Mermaid has some restriction on how to use markdown by default:

    - [markdown](https://mermaid.js.org/syntax/flowchart.html#markdown-formatting)
	  has to be enclosed into ``"` ‌`` ``‌ `"`` braces;

	- the typewriter style, i.e., `text like this`, seems not easily usable.

<!--ᚦ: [let's keep this one/three lines of Chris's here, just in case]
Guards can provide information (similar to pattern-matching) which can then be used in the action. Each guard should come with a specified type `LocalData -> Maybe<T>` where `T` is the data that the guard will bind (pattern-match) out of the local data if (and only if) it matches.
-->
<!--ᚦ: let's keep this here for the moment ¶
!!! example

	```mermaid
	flowchart TD
		check{are we below the rate limit ?}
		check -->|yes| A[match hash and »reply to address«]
	    A --> doA(["` time stamp _hash_ _reply to_ `"])
		check -->|no| B(["` no op `"])

	```

	If the rate limit is not surpassed, we answer the request.
	The matched arguments are the hash to be time stamped
	and the address to which we have to respond.

	hash

	:  matched argument


	returnAdress

	:  matched argument


	`juvix`
    ```
    if limitOK() then Some (hash,replyTo) else None ;
    ```
-->

## Action dependencies and conflict resolution

!!! note "On `Action dependencies and conflict resolution`"

    We need to describe how actions should be linearized
    if they are not all concurrent.
    In many cases,
    the conflict relation can be stated no the level
    of action tags.

    !!! info "This is about actions!"

        The relation of conflict is for
        sets of action labels (and not about guards).

    Form

    : Free form, except for that we need the code for
    the conflict resolution function (at the end).
    

## Action function (and auxiliary functions)

!!! note "On `Action function and auxiliary functions`" 

    This is essentially well-documented code
    of the actual action function.

    Form

    : One or several code fragments,
      with the action function at the end,
      interlaced with explanatory prose.


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

### Overview `{` action ⟨$i$⟩`}`

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
<!-- footnotes -->

[^1]: The specification pages impose
      a linear order on guards / action labels;
      however,
      this is independent of
      any conflict resolution strategies.

[^2]: The only exception may be some messages
      that are prescribed by the [[Application Architecture]]
      and similarly actions.<!-- todo: well, where do we have those?-->

[^2']: Eventually,
    we may want to describe each action 
    as a [series-parallel graph](https://en.wikipedia.org/wiki/Series%E2%80%93parallel_graph)
    of _action primitives;_
    the main rationale is fostering code re-use,
    the potential for parallel execution deserves mention as well.
    Finally,
    in some situations,
    we can avoid sending messages to "self".
    Thus,
    you _should_ define action primitives if they naturally arise.


[^3]: One way to structure is to have a set of "sub-actions"
      with a conflict resolution strategy.
