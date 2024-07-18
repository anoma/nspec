# [Name of non-interactive action] on [Name of guard] {V2 Template ⊂ V3 Template}

## Purpose

!!! note

	We need to give a high level description of
	when the action is activated
	and what the action is doing as a response.
	
	Form
	
	: Some short paragraphs as a summary, ideally just one. 
	More details will follow.

!!! example

	The time stamping server has a build in rate limit.
	Time stamping requests are only served 
	if the mean time between received requests is within 
	bounds that have been fixed at creation.
	

??? todo

	{move the contents of this note following to a proper place / remove it}  
	Recall that each guarded action is a pair of a guard function and an action function.
	Conceptually, the guard function has two purposes:
	first it determines whether the action that it is guarding is enabled;
	moreover, 
	if the action is enabled it provides matched arguments and an action label. 

	The action function takes the time stamped trigger, local data and matched argument as input
	and computes 

	- the updates to the engine environment
	- the set of messages to be sent
	- timers to be set, cancelled, and reset
	- new engines to be created.

	In theory,
	all guards of an engine are evaluated in parallel,
	each of which potentially triggers an the execution of the action,
	e.g., upon  arrival of new  message;
	in practice, for specific cases, one may want to choose 
	a more efficient, but equivalent strategy.

	In many simple cases,
	it is never the case that several guards become true;
	however, 
	if several actions are enabled,
	priorities of guards may be used to resolve undesireable non-determinism.
	It is necessary to mark the non-determinism if it is desired.
	Each guard comes with an associated action that is executed
	if its action is enabled (and has the highest priority).

!!! note

	Typically, new events are "muted" for the time of 
	guard evaluation and action execution.
	The only way around this is the specification of a 
	maximum duration of action processing.

## Guard

!!! note

	We need a description of conditions for the action to be enabled.
	The matched arguments, the action label, and any other precomputations.

	Conceptual structure
	
	: We essentially need a decision tree / flow chart / ... for 
	
	- how to determine whether the action is enabled, and
	
	- describe the list of matched arguments and pre-computations 
	and how they are computed along the way


	Form
	
	: There are three parts: 
	
	1. an (optional?) flow chart that matches the conceptual structure

	2. An English language description, describing the logic of the flow chart (even in absense of a flowchart) and describes each matched argument, using a [definition list](https://pandoc.org/MANUAL.html#definition-lists)
	
	3. Juvix code of the actual guard function

<!--ᚦ: [let's keep this one/three lines of Chris's here, just in case]
Guards can provide information (similar to pattern-matching) which can then be used in the action. Each guard should come with a specified type `LocalData -> Maybe<T>` where `T` is the data that the guard will bind (pattern-match) out of the local data if (and only if) it matches.
-->

!!! example

	```mermaid
	flowchart TD
		check{are we below the rate limit ?}
		check -->|yes| A[match hash and »reply to address«]
		check -->|no| B[drop request `no op`]
	```

	If the rate limit is not surpassed, we answer the request.
	The matched arguments are the hash to be time stamped
	and the address to which we have to respond. 


	```juvix
	if limitOK() then Some (hash,replyTo) else None ;
	```

## Action(s) `{` possibly plural!!! `}`

!!! note

	The guard _may_ have a complicated tree-like structure.
	If there are several natural distinct cases 
	each of which are a (sub-)action,
	then we may actually have a set of actions
	under the same guard.
	
!!! example

	There is always the `no op` opeartion as default,
	which just drops the message.


## [Action name $i$] [action label $i$] `{each action i needs a label for the LTS anyway}`

!!! note 
	
	The description of the actions starts 
	with an English language highlevel description,
	followed by more detailed descriptions
	of state update, messages to be sent, timers to be set/cancelled/reset,
	and engine instances to be spawned.
	The code is at the very end.

### Overview

!!! note

	Some paragraphs of English language prose
	as the author sees fit.

!!! example

	Besides answering the request,
	we have to update the ringbuffer of the mailbox state.

??? todo

	{update and move the following to the proper place}
	The action of a guarded action is a function $f_{act}$.
	It takes as input
	all local data of an engine _and also_
	the _arguments_ that are returned by the guard.
	In more detail, the list of inputs is

	- matched arguments
	- external + internal ID of the engine itself (unchangeable)
	- the "event trigger"
		- message received or
		- timer "handle(s)" of elapsing timer(s)
		- engine-specific local state
		- local time (when guard evaluation started)
		- mailbox contents and their optional state (for every mailbox)
	- remembered timers with their scheduled time
	- acquaintances (known other engine instances)
	- a (finite) map from names to external IDs

	The output of the action describes after the event has finished

	- updates to the above local data (except for identities and arguments)
	- a finite set of messages to be sent
	- a finite set of engines to be spawned, setting
		- engine type
		- initial state
		- a name for the process (that is unique relative to the engine)


!!! todo

	establish some proper reciprocal linking scheme here 
	
	<!--
	make PR for https://github.com/anoma/formanoma/tree/heindel/engine-locale
	-->	


!!! todo

	simple juvix code example of client server

!!! todo
	
	add details according to the discussion in the PR,
	see e.g., here https://github.com/anoma/nspec/pull/84#discussion_r1639785764
	

### Effects

!!! note

	We give quick descriptions of the effects.

#### state update

!!! note

	Describe the state update
	
!!! example

	The rate limit is constant in the example.

#### messages to be sent

!!! note

	Describe the messages to be sent
	as a list (or a set if you prefer).
	
!!! example

	We send only a single message. 
	
	- Send the time stamped hash to the requested »reply to« address.
	
#### engines to be created

!!! note

	Describe the engines to be created.

!!! example

	No engines are created.

#### timers to be set/cancelled/reset 

!!! note

	Describe the engines timers to be set/cancelled/reset.
	
!!! example

	The time stamping server does not need to set any timers.
	
### Code	

!!! note

	Last but not least,
	the actual code of the model implementation.
	
??? example

	```juvix
	;
	```
