---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - engine
  - mailbox
  - engine-instance
  - engine-type
  - guarded-action
  - engine-acquaintances
---

# On Engines in the Anoma Specification

## Introduction: on actors and engine instances

The Anoma specification is inspired by the actor model[^3]
where systems consist of _actors_ that communicate via message passing.
An Anoma node instance is modelled as a finite[^4] collection of
_engine instances_ that communicate by sending messages to each other,
very much like actors do, 
but subject to some "fine print" that we shall cover in due course.
The behaviour of each engine instance—i.e., 
how it reacts to receiving a message in 
the context of previously sent messages—is
determined by a _state transition function,_
reminiscent of the next-state function of
[finite state machines](https://en.wikipedia.org/wiki/Automata_theory#Formal_definition) 
(or rather [Moore machines](https://en.wikipedia.org/wiki/Moore_machine#Formal_definition)), 
defined formally as an [Isabelle/HOL-locale](https://github.com/anoma/formanoma/blob/1b9fa7558ce33bb4c2e4d31277255cdeabbc59b5/Types/Engine.thy#L215),
and is explained in more concrete terms in
the guarded action template below. <!-- 
some of these links need "continous" updating [do not erase this comment] 
--> Each invokation of a state transition function
corresponds to an event (in the sense of the actor model theory);
events are _triggered_ at the engine instance
by the arrival of a new message[^1] or an elapsing timer;
the result of applying the state transition function 
describes 
not only the state update of the engine instance,
but also which further actions need to be taken: 
sending of messages, setting timers, and creating new engine instances.[^10]

The Anoma specification describes
a ꜰɪxᴇᴅ finite number of _engine families_
such that every (correct and non-faulty) engine instance in an Anoma instance
belong sto a unique family that describes its behavior by a set of guarded actions;
these engine families are static,
while dynamic parameters at engine creation determine the exact behavior.
<!-- add footnote to engine system locale ["axiom" state_partition](https://github.com/anoma/formanoma/blob/915039faa7cfe77c2998b309ef65b671e604fead/Types/Engine.thy#L192) -->
<!-- this be moved elsewhere
!!! definition 
¶
	We call the set of all engine instances that share the same state transition function the _engine type_ of the state transition function.
-->
We start by describing in more detail the "internal" structure of
each engine instance, and the accompanying design choices.
Then we describe state transition functions in more detail
before we finally come to how
we actually will specify state transition functions in the anoma specification
via sets of guarded actions.

## On the local data of engine instances: the engine environment

Each engine instance has the following local data that it can 
access directly and exclusively
at any given moment while processing event triggers:

- its _name_, which must be globally unique and 
  _may_ be given by an ordered pair of<!--
  cf. https://github.com/anoma/formanoma/blob/a00c270144b4cfcf2aea516d7412ffbe508cf3d1/Types/Engine.thy#L208-L209-->

    - a child name, chosen by the parent engine instance at creation
    - the parent's globally unique name

- a mailbox cluster, represented by a partial map with a finite domain of definition <!--
  cf. https://github.com/anoma/formanoma/blob/a00c270144b4cfcf2aea516d7412ffbe508cf3d1/Types/Engine.thy#L211-->

    - from _mailbox identifiers_ (**MID** for short)

      
    - to the type of _mailboxes_, which in turn is 
		- a list of messages (that were sent to the MID but not processed yet)
		- an optional mailbox-specific state (for quick processing of incoming messages)

  - a finite set of _acquaintances_[^2] represented by<!--
	cf. https://github.com/anoma/formanoma/blob/a00c270144b4cfcf2aea516d7412ffbe508cf3d1/Types/Engine.thy#L213
  -->

    - a finite set of names <!-- ᚦ: TODO: figure out how to combine with aliasing -->

- memory for previously set timers, given by<!--
  cf. https://github.com/anoma/formanoma/blob/a00c270144b4cfcf2aea516d7412ffbe508cf3d1/Types/Engine.thy#L212-->

    - a finite list of timers

<!-- 
ᚦ: whp, we do not need this any more (no more necessity of crypto ids) 
--><!--
- memory for names of spawned engines that 
  do not have a cryptographic ID yet--><!--
    cf. https://github.com/anoma/formanoma/blob/a00c270144b4cfcf2aea516d7412ffbe508cf3d1/Types/Engine.thy#L213 needs 'ext_id option though as codomain type of the fmap-->

- engine-specific local state<!--
  cf. https://github.com/anoma/formanoma/blob/a00c270144b4cfcf2aea516d7412ffbe508cf3d1/Types/Engine.thy#L209 -->

<!-- ᚦ: ooof, this was still here ... and bye bye--><!--
- the current time[^7]--><!--
  cf. https://github.com/anoma/formanoma/blob/a00c270144b4cfcf2aea516d7412ffbe508cf3d1/Types/Engine.thy#L210-->

The record of all these local data is called the _engine environment._[^11] 
The types are formalized in the [`single_engine`-locale](https://github.com/anoma/formanoma/blob/f70a041a25cfebde07d853199351683b387f85e2/Types/Engine.thy#L205),
 with a translation from the Juvix code.<!--
 link **will** need updating [ᚦ do not erase this comment] OUT OF DATE ALERT!
-->
The engine instance's name is unchangeable,
once the engine is created;
every correct implementation must ensure that
the parent engine chooses a globally unique name before an engine can be created,
e.g., 
by using the pair of its own globally unique name,
paired with a name that is unique among its children—<!--
-->either spawned previously or in the future.
Should the need arise for changing the name of an engine
(as it has been sent to undesired destinations),
a new *"continuation engine"* can be spawned with a new name;
we shall describe this in more detail after introducing 
transition functions.

## On transition functions of engine instances

The Anoma Specification uses pure functions to describe
the atomic computation that each engine instance performs when
a new message is ready to be processed or
a notification from the local clock is received;
moreover,
the transition function also encodes the changes to its local environment.
The formal version is
(any interpretation of) the [`transition_function`](https://github.com/anoma/formanoma/blob/75331d688f2ae399fbebb008549b2dfda78b4e5b/Types/Engine.thy#L217) of
the [`single_engine`-locale](https://github.com/anoma/formanoma/blob/f70a041a25cfebde07d853199351683b387f85e2/Types/Engine.thy#L205).

### Inputs of a transition function

Transition functions take two chunks of data as input:
the local state and the (time stamped) 
[_trigger,_](https://github.com/anoma/formanoma/blob/f70a041a25cfebde07d853199351683b387f85e2/Types/Engine.thy#L19)
which is either a message that was received (and is to be processed) or
a notification from the local clock about
the elapsing of a non-empty set of timers.<!--
	make a design choice of whether
	the message is "automatically" added to the mailbox
-->
Each trigger comes with the local time when 
the event is triggered,
which we may think of as "now".

_Digression on time_  <!-- 
line break 
-->The only information about local wall-clock time in 
the input of the transition function 
is

- "now"—the [time](https://github.com/anoma/formanoma/blob/f70a041a25cfebde07d853199351683b387f85e2/Types/Engine.thy#L222) stamp of the trigger—and 
- the set of previously set timers, 
  each of which has a
  [_handle._](https://github.com/anoma/formanoma/blob/f70a041a25cfebde07d853199351683b387f85e2/Types/Engine.thy#L24)

!!! note

	The treatment of local wall-clock time is still in alpha stage, 
	but we may need it to mitigate possible limitations of
	the partial synchrony abstraction
	(see, e.g.,
	[The Economic Limits of Permissionless Consensus](https://arxiv.org/pdf/2405.09173)).
	There are also subtleties concerning 
	monotonicity of clock implementations in
	common operating systems.


### Outputs of a transition function

We describe the outputs in two steps:
first,
we cover _absolutely pure_ transition functions,
which do not require any source of (true) randomness
or direct inputs from the phyiscal device the engine instance is running on;
then, we follow up on 
how engine-local sources of input or randomness can
affect the choice of actions to be taken.

#### Outputs of absolutely pure transition functions

The output of an absolutely pure transition function
has five components:
the update to the local data, 
messages to be sent,
update of the timers set (new ones to set, old ones to cancel),
new engine instances to be spawned,
the (estimated) duration of the event.

##### Timers to be set

Given the inputs,
the transition function may decide to set new timers
and "remove" old timers.
As each timer has an engine-local handle,
this amounts to updating the map of local timers, 
cancelling superseded timers and
adding new timers.
Handles should only be used once during the life-time of 
an engine instance.
The type of this component of the output is
a [map from handles to points in local time](https://github.com/anoma/formanoma/blob/4ad37bc274ad25e64d15fe5f00dbd7784e339ce0/Types/Engine.thy#L230).

##### Engine instances to be spawned

If new engine instances should be spawned,
the engine instance that is requesting to spawn the new instances is
the _parent engine instance_ (or just _parent engine,_ 
for short)
and the newly spawned instance are children.
The following data need to be given for a newly spawned engine.

- the _initial state_ that the child engine instance
  (the one it will be in when it receives the first trigger)
- a _name_,
  unique throughout the life-time of the parent engine instance. 

The engine instance will become "alive" 
after the current execution of the transition function.

The engine allows addressing messages to
the engine to be spawned (before it is alive),
which brings us to the next point.

##### Messages to be sent

This is a finite set of _enveloped_ messages,
each of which carries information about the intended recipient
and the mailbox of the latter.
The recipient can be picked either by an external identifier or a name.
All formalities of messages are in the [`Message.thy`-theory](https://github.com/anoma/formanoma/blob/heindel/engine-locale/Types/Message.thy)<!--
	link will need updating
-->.


##### Updates to local data

Last but not least, 
all local data can be updated—except for the engine identities.

### Outputs of interactive transition functions

As implementations may want to have access to "true" randomness,[^8]
we need a way for engine instances to have access to randomness.
For this,
transition functions may make use the mathematical counterpart 
of $n$-sided dice.
Moreover,
engine instances need to interact with the user 
_synchronously,_
typical for final confirmations of important actions 
or interaction with hardware security modules.
Such interactions with _external_ streams of input 
are a second kind of interaction,
and it is made possible by providing users with a finite number of choice at a time.
Finally, 
there may be a mix of inputs and randomness.
For example and engine may generate a random username and 
the user is asked to accept or choose it manually.

In summary,
instead of directly producing the `Outputs of absolutely pure transition functions`,
we have a finitely branching tree 
whose laves are `Outputs of absolutely pure transition functions`
and whose inner nodes are either requesting the user to pick one of a finite number of choices
or the rolling of some $n$-sided dice.[^9]

## Transition functions via guards and actions =: guarded actions

The Anoma specification defines transition functions
via a set of guarded actions.
The word `guarded` is taken from Dijkstra's 
[_guarded_ command language (ɢᴄʟ)](https://en.wikipedia.org/wiki/Guarded_Command_Language),
`action` is taken from Lamport's 
[temporal logic of _actions_ (ᴛʟᴀ⁺)](https://lamport.azurewebsites.net/tla/tla.html),
and indeed, guarded actions are a mix of the two;
the notion of action (together with local data) allows us to
express properties in the temporal logic [ᴄᴛʟ*](https://en.wikipedia.org/wiki/CTL*),
while guards emphasise that actions have clear pre-conditions,
and we may also use [weakest-precondition calculus](https://en.wikipedia.org/wiki/Predicate_transformer_semantics),
e.g., for deriving invariants.

<!--
The basic idea of guarded actions is to split up
the set of possible inputs of the state transition function into
a finite number of cases, 
each of which corresponds to an _event kind_—very much like
the transitions of a [Petri net](https://en.wikipedia.org/wiki/Petri_net#Execution_semantics)
can be "unfolded" into an [event structure](https://dl.acm.org/doi/abs/10.5555/898126),
where events are _occurrences of transitions_ of the original net.
-->
The basic idea of guarded actions is to describe 
the state transition function in a modular way
such that each (non-trivial) state transition corresponds to 
the execution of (at least) one guarded action.[^6]
The guard of a guarded action specifies the precondition of the action,
which describes what state changes should happen when the guard is triggered.
However,
guarded actions may be concurrent or in conflict with each other,
and this situation need to be handled with care.
The details of guarded actions are explained in the [[Guarded Engine Template]].

## On engine types

An engine type is in bijective correspondence to a function that
describes how every instance that is based on this function behaves;
we may just speak of an engine type as if it was a function.
This function takes as input all local data of engine instances. 
Each item of local data falls into one of the following three categories:

- information that is not changed (as part result of mere state transition):
    - the cryptographic identity
- specific information about the event that has occurred
    - for a message, the time of arrival and the actual message
    - for a timer that has elapsed, the _handle_ of the timer
- all other local data (as described above in the section
  `On the local data of engine instances`)

<!-- 

As this function is strongly typed in the formal model / in juvix, 
the engine type thus determines a list of types, which seems long.
Thus, let us "annotate" the above list.



!!! todo

	clean up the following annotated quote (ignore for the review for the moment) 🙏

> - an {engine independent type for the} identity, namely a pair of
>     - an external identity {type} and
>     - an internal identity {type}
> - {types for} mailboxes that store received messages in a list in more detail
>   - a finite set of mailboxes, typically non-empty {from a finite set of types
>     for mailbox contents---not to be confused with mailbox types}
>   - a map from (engine-relative) mailbox identifiers to the above mailboxes
>     {so a function type `mailbox identifier type` => `mailbox type list`}
>   - optionally, each mailbox may have a mailbox-state {i.e., the function type
>     is actually `mailbox identifier type` => `(mailbox state type) * (mailbox
>     type list)`}
> - a finite set of _acquaintances_ (borrowing actor terminology), in more
>   detail
  >   - a finite set of names {hence a type `ac_name`}
  >   - a map from names to the identities of an engine instance {we have all
  >     those types already}
> - a local clock {we assume one, and we do not have to do anything here}
> - memory for previously set timers (that are still relevant) {a type of `timer
>   handles`}
> - memory for spawned processes that do not have a cryptographic identity yet
>   {here we should probably just re-use the name type for acquaintances}
> - engine-specific local state {the one type `state` that is "really" specific
>   to each engine}

-->

Besides updates to the changeable data, the transition function produces

- requests for spawning new engines
- the messages to be sent
- the timers to be set on the clock


## The conceptual structure of each Engine Type page in the specs

As a short synopsis, the structure of each engine type page 
starts with a big picture, some examples, and then the details.
A table of contents has the following structure.

- engine type name (e.g., _Auctioneer_)
  - purpose {very big picture}
  - list of engine-specific types
    - local state
	- message types received and sent
    - mailbox state types (for optimisations)
  - message sequence diagram(s) {specific example(s)}
  - conversation diagram {big picture}
    - conversation partners
        - partner A
    		- incoming 
	    	    - A1
		        - ...
		        - Anₐ
      		- outgoing 
                - A1
 		        - ...
    		    - Amₐ
	    - ...
	    - partner X
	        - incoming 
	            - X1
     		    - ...
	    	    - Xnₓ
		    - outgoing 
		        - X1
    		    - ...
	    	    - Xmₓ
  - guarded actions {now for the details}
    - guarded action α1 (e.g., receive bid)
  	    - guard α1 {`local data * trigger → arguments option`}
	    - action α1 {`local data * arguments → local data update * sends * timers * spawns`}
	        - local data update {prose}
            - messages to be sent {prose}
		    - timer to be set {prose}
		    - engines to be spawned {prose}
	- ...	
    - guarded action αk (e.g., finalise auction)
  	    - guard αk {`local data * trigger → arguments option`}
	    - action αk {`local data * arguments → local data update * sends * timers * spawns`}
	        - local data update {prose}
            - messages to be sent {prose}
		    - timer to be set {prose}
		    - engines to be spawned {prose}

## Template files


??? "Engine template"

    !!! info 

        The following template can be found in the `overrides/templates/engine-template.md` file.
    

    --8<-- "./../overrides/templates/engine-template.md:6"

??? "Guarded action template"


    !!! info 

        The following template can be found in the `overrides/templates/guarded-action-template.md` file.

    --8<-- "./../overrides/templates/guarded-action-template.md"


---

<!-- footnotes -->

[^1]: We also will allow for elapsing of timers,
which is a technical detail concerning the handling of 
local time in engine instances.
The role of the template is the organisation of 
the specification of engine types and their engine instances.

[^2]: Here, we borrow actor terminology.

[^3]: At the time of writing V2 specs, further relevant sources are *Selectors:
Actors with Multiple Guarded Mailboxes*[@selectors-actors-2014] and *Special
Delivery: Programming with Mailbox Types*[@special-delivery-mailbox-types-2023].
We shall refer to the latter as _mailbox usage_ types to avoid a name clash with
the type of messages that are contained in mailboxes.

[^4]: The specification does not fix any bound on 
	the number of engines in existence.

[^5]: Note that in TLA⁺, pre-conditions of actions are
	present in the guise of the `ENABLED` predicate. 

[^6]: Arriving messages that do not trigger any "non-trivial" guarded action
	are added to the mailbox they are addressed,
	time is incremented by a default delay, and nothing else changes.


[^7]: Local time is still in alpha stage, 
	but it could be used to implement busy waiting;
	however,
	the preferred way to interact with the local clock is
	setting new timers for specific points in local time.
	Probably, 
	this should be replaced by minimal and maximal duration for an event
	for the specification of real time engines.

[^8]: A well-known example for relevance of sources of "true" randomness are
	[cloudflare's lava lamps](https://www.cloudflare.com/learning/ssl/lava-lamp-encryption/).

[^9]: See the
	[`local_interaction`data type](https://github.com/anoma/formanoma/blob/f70a041a25cfebde07d853199351683b387f85e2/Types/Engine.thy#L53).

[^10]: Here, we follow the terminolgy of event-driven state machines of using
	a single function where in Mealy machines, we have a pair of functions,
	one for the state update and one for the outputs generated.

[^11]: Clocks are a little more complicated to get into the picture;
	they are "external" to the environment
	and still epxerimental.
