# [Name of non-interactive action(s)] on [Name of guard] `{`V2 Template ⊂ V3 Template`}`

## Purpose

!!! note

	We need to give a high level description of
	when some actions are activated
	and the effects of the actions to be performed.
	
	Form
	
	: Some short paragraphs as a summary, ideally just one. 
	More details will follow.

!!! example

	The time stamping server has a build in rate limit.
	Time stamping requests are only served 
	if the mean time between received requests is within 
	bounds that have been fixed at creation,
	which is not present in V2.

!!! note

	Typically, new events are "muted" for the time of 
	guard evaluation and action execution.
	The only way around this is the specification of a 
	maximum duration of action processing.

## Guard

!!! note

	We need a description of under which conditions actions are enabled;
	for each case, 
	we need to describe the matched arguments,
	the action label, 
	and any other precomputations.

	Conceptual structure
	
	: We essentially need a decision tree, flow chart, or similar for 
	
	- how to determine whether an action is enabled (and which one), and
	
	- describe the list of matched arguments and pre-computations 
	and how they are computed along the way.


	Form
	
	: There are three parts: 
	
	1. an (optional?) flow chart that matches the conceptual structure

	2. an English language description of the logic
	that the flow chart illustrates (even in absense of a flowchart) and
	also descriptions of the  matched argument,
	using a [definition list](https://pandoc.org/MANUAL.html#definition-lists)
	as in the example below.
	
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
	
	hash
	
	:  matched argument
	
	
	returnAdress
	
	:  matched argument
		

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
	
	
 <!--!!! example
¶
	There is always the `no op` opeartion as default,
	which just drops the message.
-->

## [Action name $i$] [action label $i$] `{each action i needs a label for the LTS anyway}`

!!! note 
	
	The description of the actions starts 
	with an English language high-level description,
	followed by more detailed descriptions
	of state update, messages to be sent, timers to be set/cancelled/reset,
	and engine instances to be spawned.
	The code in collapsed form is put after the overview.

### Overview

!!! note

	Some paragraphs of English language prose
	as the author sees fit.

!!! example

	Besides answering the request,
	we have to update the ringbuffer of the mailbox state.

    ??? "show me the code"
	
	```juvix
	;
	```

<!-- ᚦdon't think we need this any more
!!! todo

	simple juvix code example of client server
-->	
	

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
	
