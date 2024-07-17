---
icon: octicons/project-template-24-1337
search:
  exclude: false
---

# Engine Family [_X_] {V2 Template}

## Purpose {of members of engine family _X_}

!!! note

	The purpose describes in broad terms what the role of this engine family is in context,
	be it

	- in relation to other engine instances within an Anoma node and/or

	- in the whole Anoma instance at large.
	
	Form
	
	: The purpose is a couple of short paragraphs of prose, possibly just one.
	
!!! todo

	polish example 👇 

??? example

	A generic engine family _X_ will want to have a purpose,
	such as responding to requests from a client
	and hence _X_ = `Server`.
	

## Specific types {of engine familiy _X_}

!!! note

	This section describes all types—or type parameters, to be precise—that
	are specific to an engine family.
	However, 
	if several engine families share the same types,
	the best place is either

	- the lowest common ancenstor that the engine families share in 
		the engine family hierarchy, or

	- a more suitable place, if that is not an option, 
		e.g., if it is one of the [[Basic Types]].
		
	Form
	
	: You may want to provide an overview of how things relate to each other.

### Engine-specific state type

!!! note

	The engine-specific state type is usually 
	tailor made for each engine family.
	
	Form
	
	: Either a definition of the type in Juvix, or a link to such a definition. 
	Moreover, here we want descriptions of the data structures 
	in English language.


### Message type(s)

!!! note

	Next, we describe all the message types that members of family _X_ 
	are able to process, in principle.
	For each such "receivable" message type, 
	we want
	
	- a _message tag_ 
    - a list of _argument types_ 
	- a (default value for a) _formal parameter name_ for each element of the list of _argument types_

	The term `message tag` is borrowed from  the [Special Delivery paper](https://dl.acm.org/doi/abs/10.1145/3607832)). 
	The list of argument types has to be uniquely determined by the message tag.
	
!!! todo

	spell out the form, although natural

### Mailbox state type(s) {optional}

!!! note
	
	Mailboxes of engines may have mailbox state.
	If so, here is the place to describe them.
	In fact, this is actually a list of different mailbox states
	in that each mailbox may have a mailbox specific state.

## [Title of Paradigmatic message sequence diagram] {optional}

!!! note

	We can use one or more message sequence diagrams to show how
	members of the engine family exchange messages with other engine instances, 
	typically from different engine families.
	The general idea is that
	each message sequence diagram in the engine type page describes
	a pattern for test cases.

??? example "Client-Server Example"

    In the below _Client-Server_ example,
    the message sequence chart expresses the possibility of a message exchange,
    where the server responds to the request of the client;
    every implementation has to have a matching execution/run.
    A good practical example for how
    an actor system (or a formal model of it) gives rise to sequence diagrams
    is [stateright](https://www.stateright.rs/)'s [state explorer](https://www.stateright.rs/seeking-consensus.html#stateright-explorer).


    We can use
    [`mermaid` sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html) 
    to draw [message sequence diagrams](https://www.uml-diagrams.org/sequence-diagrams.html),<!--
    see e.g., https://moves.rwth-aachen.de/teaching/ws-21-22/fuml/  
    - https://www.researchgate.net/profile/Joost-Pieter-Katoen/publication/221305522_Pomsets_for_MSC/links/5778102608aead7ba07461af/Pomsets-for-MSC.pdf
    - our formal model should have a precise notion of these as well, 
      in particular if a given one can actually happen in our model
    -->
    using the `-)`-syntax by default,
    expressing that message sending is "asynchronous"[^1].
    The message sequence chart should be included for
	engines at the top of the engine familiy hierarchy;
    it is optional for engine families at the bottom of the hiearchy.
    A simple illustrative example is
    the request-response pattern.
	A more complex example is given in the [[Engine Template Example]].
    
	```mermaid
    sequenceDiagram
        participant Client
        participant Server
        Client-)Server: read request for key α
      Server-)Client: current value of α is ζ
      Note right of Server: A blockchain is a data base after all.
    ```

??? example "Several Engines Example"

    The following is a good example of a larger diagram,
    which concerns a larger number of engine families
    taken from the
    [v1 specs](https://specs.anoma.net/v1/architecture-2/ordering-v1.html#a-life-cycle-with-some-details).

    ```mermaid
    sequenceDiagram
        participant User
        participant Worker
        participant ExecutionSupervisor
        participant ExecutorProcess
        User-)Worker: TransactionRequest
        Worker--)Worker: fix batch №
        Worker-)User: TransactionAck
        Worker--)Worker: Buffering & Shuffling
        Worker--)Worker: fix tx №
        Worker-)ExecutionSupervisor: spawnExecutor
        ExecutionSupervisor-)Worker: EPID
        Worker-)ExecutorProcess: ExecuteTransaction
        Worker-)Shard: KVSAcquireLock
        Shard-)Worker: KVSLockAcquired
        Worker-)Shard: UpdateSeenAll
        activate ExecutorProcess
        ExecutorProcess-)Shard: KVSReadRequest
        Shard-)ExecutorProcess: KVSRead
        ExecutorProcess-)Shard: KVSWrite(Request)
        %%    ExecutorProcess-)WhereToIdontKnow: pub sub information of execution data
        ExecutorProcess-)User: ExecutionSummary
        ExecutorProcess-)Worker: ExecutorFinished
        deactivate ExecutorProcess
    ```


	One may take a pre-existing diagram and
    "cut out" a portion or 
    mark it as in the following variation of the previous diagram.


    ```mermaid
    sequenceDiagram
        participant User
        participant Worker
        participant ExecutionSupervisor
        participant ExecutorProcess
        User-)Worker: TransactionRequest
        Worker--)Worker: fix batch №
        Worker-)User: TransactionAck
        Worker--)Worker: Buffering & Shuffling
        Worker--)Worker: fix tx №
        rect rgb(191, 223, 255)
          note right of Worker: ExecutionSupervisor in action
          Worker-)ExecutionSupervisor: spawnExecutor
          ExecutionSupervisor-)Worker: EPID
        end
        Worker-)ExecutorProcess: ExecuteTransaction
        Worker-)Shard: KVSAcquireLock
        Shard-)Worker: KVSLockAcquired
        Worker-)Shard: UpdateSeenAll
        activate ExecutorProcess
        ExecutorProcess-)Shard: KVSReadRequest
        Shard-)ExecutorProcess: KVSRead
        ExecutorProcess-)Shard: KVSWrite(Request)
        %%    ExecutorProcess-)WhereToIdontKnow: pub sub information of execution data
        ExecutorProcess-)User: ExecutionSummary
        ExecutorProcess-)Worker: ExecutorFinished
        deactivate ExecutorProcess
    ```

## Conversation Diagram {optional}

!!! note

	As a birds eye view of all possible message exchanges between 
	engine instances of several families,
	we can draw a graph whose nodes are labelled with engine families
	and whose edges are labelled with message types (possibly with message tags).
	For each labelled edge,
	there must be some some admissible message sequence diagram
	such that a message is sent from an engine of the source engine family
	to the target engine family.
	We borrow the term conversation diagram from
	[business process modeling](http://dx.doi.org/10.1016/B978-0-12-799959-3.00021-5).
	The conversation diagram of an engine page only contains edges 
	that have engine family _X_ as source or target.



??? example "Conversation Diagram"

	Taking again the example of workers in Narwhal,
	the worker is in communication with other workers,
	the user and the primary. 
	A partial diagram would be the following.

	```mermaid
	erDiagram
		PrimaryX }|--|| WorkerX1 : WorkerHash
		WorkerX1 ||--|{ MirrorY1 : NewTransaction
		User ||--|{ WorkerX1 :  TransactionRequest
	```

!!! note

	The information from the conversation diagram could be taken from
	the list of conversation partners,
	each with a list of incoming and outgoing messages,
	relative to the current engine family _X._
	This is not yet implemented though.
	
## Guarded Actions

!!! note

	By default, guarded actions should be inlined in the same page. If an engine has
	too many guarded actions (and thereby putting them all in one page would be
	unworkable), they can be split out into separate files and linked.

!!! todo

	put link(s) to the guarded action template


### [Guarded action $1$]

<details>
  <summary>[single phrase on guarded action $1$]</summary>
  <p>[Guarded action one description]</p>
</details> 

.  
.  
.  

### [Guarded action $n$]

<details>
  <summary>[single phrase on guarded action $n$]</summary>
  <p>[Guarded action $n$ description]</p>
</details> 


[^1]: By default,
	we are working actually with the partial synchrony abstraction,
	which in first approximation is closer to the asynchronous case
	as even after global synchronisation time,
	we cannot know how long we would have to wait for responses to messages sent.
