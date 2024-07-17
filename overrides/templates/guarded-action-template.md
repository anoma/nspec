# [Name of non-interactive action] on [Name of guard] {V2 Template ⊂ V3 Template}

## Purpose

!!! note

	We need to give a high level description of
	when the action is activated
	and what the action is doing as a response.
	
	Form
	
	: One paragraph as a summary. More details deferred to later.


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

!!! Note

	Typically, new events are "muted" for the time of 
	guard evaluation and action execution.
	The only way around this is the specification of a 
	maximum duration of action processing.

## Guard


!!! note

	We need a description of conditions for the action to be enabled.
	The matched arguments, the action label, and any other precomputations.


!!! todo

	Conceptual structure


!!! todo

	actual form

<!--ᚦ: [let's keep this one/three lines of Chris's here, just in case]
Guards can provide information (similar to pattern-matching) which can then be used in the action. Each guard should come with a specified type `LocalData -> Maybe<T>` where `T` is the data that the guard will bind (pattern-match) out of the local data if (and only if) it matches.
-->

## Action [ActionLabel] {each action needs a label for the LTS anyway}

!!! note 
	
	A description of the action is necessary,
	ideally complemented with juvix code.


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
	

### state update

!!! note

	describe the state update

### messages to be sent

!!! note

	describe the messages to be sent
	
### engines to be created

!!! note

	describe the engines to be created

### timers to be set/cancelled/reset 

!!! note

	describe the engines timers to be set/cancelled/reset 
