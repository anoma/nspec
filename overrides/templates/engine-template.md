---
icon: octicons/project-template-24-1337
search:
  exclude: false
---

??? info "Juvix"

	<!--```juvix-->
    ```
    module overrides.templates.engine-template;
    ```

# [family name] Engine Family

## Purpose

!!! note

	The purpose should describe in broad terms what
	the role of (any member of) this engine family is

	- in relation to other engine instances within an Anoma node and/or

	- as part of the whole Anoma instance at large.
	

	Form
	
	: The purpose description is in the form of some short paragraphs of prose, possibly just one.

	Conceptual Structure
	
	: One relatively self-contained piece of prose,
	providing links to techincal terms and unavoidable jargon.

	
!!! example

	# Time Stamping Server Engine Family 

    Members of the _time stamping server_-family are accepting 
	time stamping requests for fixed size hashes 
	that clients provide as part of their time stamping requests.
	Request are answered with a response, 
	consisting of the pair of the hash and the reception time stamp,
	signed by the time stamping server instance.
	The service has a rate limit that is set at creation.

## Specific types `{`of engine familiy [family name]`}`

!!! note

	The (sub-)subsections of this section describe 
	all types—or type parameters, to be precise—that are
	specific to engine family [family name].
	However,
	if several engine families share a type,
	the best place to place the definition is either

	- the lowest common ancenstor that the engine families share in 
		the engine family hierarchy, or

	- a more suitable place, if that is not an option, 
		e.g., if it is one of the [[Basic Types]].
		
### Overview `{`optional`}`
	
!!! note

	You may want to provide an overview of how things relate to each other.

	Form
	
	: free form

### Engine-specific state type

!!! note

	The engine-specific state type is usually 
	tailor made for each engine family.
	
	Form
	
	: Either a new definition of the type in Juvix, or an included code snipped with a link where it is defined. 
	Moreover, here we want descriptions of the data structures 
	in English language, or a link to a wikipedia-page or similar.
	
!!! example
 
 
	We use the state of the time stamping server 
	to store the rate limit
	(that we assume to be static for the sake of simplicity).
	

	<!--```juvix-->
    ```
	TimeStampingServerState := Nat;
    ```

!!! warning
	
	The local clocks of engine instances are "external" to engine instances.
	If you need information about wall-clock time,
	you can only keep track of "time stamps"
	of triggers.
	Use clocks only if necessary.
	Hoever, each Anoma node may at some point in time have
	a node-wide wall-clock time service.
	

### Message type(s)

!!! note

	Next, we describe all the message types that members of family [family name] 
	are able to process, in principle.
	For each such "receivable" message type, 
	we want
	
	- a _message tag_
    - a list of _argument types_
	- a (default value for a) _formal parameter name_ for each element of the list of argument types

	The term `message tag` is borrowed from 
	[the Special Delivery paper](https://dl.acm.org/doi/abs/10.1145/3607832). 
	The list of argument types has to be uniquely determined by the message tag (at least within this engine family).
	
	Form

	: We have exactly one level four heading `#### [Message Tag]` for each receivable message type. 
	The content has two parts.
	
    1. Part one is given in the _form_ of a [definition list](https://pandoc.org/MANUAL.html#definition-lists) in the sense of markdown
	(see also [here](https://stackoverflow.com/q/28057101)) 
	where the "terms" are the formal parameter name defaults, 
	and the definitions are a short English language description of the role (and type) of the parameter, plus the type definition (with a link to where it is defined—if applicable).
	
    2. Part two provides (optional) additional information, 
	e.g., design choices, explanation of the naming process, etc.


!!! example

    #### TimeStampingRequest
	
	clientHash 
	
	: The client hash to be time stamped.
	
	    <!--```juvix-->
		```
     	clientHash : BitString;
    	```

	returnAddress
	
	: The address that the time stamped hash should be sent to.
	
	    <!--```juvix-->
		```
     	returnAdress : BitString;
    	```

	We are only using bit strings for simplicity.

### Mailbox state type(s) `{`optional`}`

!!! note
	
	Mailboxes of engines may have mailbox state.
	If so, here is the place to describe them.
	In fact, this is actually a list of different mailbox states
	in that each mailbox may have a mailbox specific state.
	
	Form
	
	: A list of type definitions and explanatory prose;
	the explanatory prose is preceding the type definition.
	
	
!!! example

	- Each mailbox has a ring buffer to estimate 
	the frequency of time stamping requests.
	
??? todo

	add juvix code for a ring buffer for this example ☝️ 

## [Title of Paradigmatic message sequence diagram(s)] `{`optional`}`

!!! note

	We can use one or more message sequence diagrams to show how
	members of the engine family exchange messages with other engine instances,
	typically from different engine families.
	The general idea is that
	each message sequence diagram in the engine family page describes
	a pattern for test cases.
	We can use
    [`mermaid` sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html) 
    to draw [message sequence diagrams](https://www.uml-diagrams.org/sequence-diagrams.html),
    using the `-)`-syntax by default,
    expressing that message sending is "asynchronous".
	For more on how
    actor systems (or models of them) give rise to sequence diagrams,
    consider exploring systems using
	[stateright](https://www.stateright.rs/)'s [state explorer](https://www.stateright.rs/seeking-consensus.html#stateright-explorer).


!!! example "Time Stamping Service"

	A member of the time stamping server family 
	may respond slightly delayed.

    
	```mermaid
    sequenceDiagram
        participant A as GenericClientA
        participant Server as TimeStampingServer
        participant B as GenericClientB
		participant C as GenericClientC
        A-)Server: TimeStampingRequest for 123 to B
        B-)Server: TimeStampingRequest for 234 to C
		Server-)B: TimeStampingResponse (8:00 AM, 123)
		Server-)C: TimeStampingResponse (8:01 AM, 234)
      Note right of Server: A blockchain is a time stamping service after all.
	```

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

## Conversation Diagram `{`optional`}`

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
	that have engine family [family name] as source or target.



??? example "Worker Communication in Narwhal"

	In the Narwhal mempool protocol,
	the worker is in communication with other workers,
	the user and its primary. 
	A partial diagram would be the following.

	```mermaid
	erDiagram
		PrimaryX ||--|| WorkerX1 : WorkerHash
		WorkerX1 ||--|| MirrorY1 : NewTransaction
		User ||--|| WorkerX1 :  TransactionRequest
	```

!!! note

	The information from the conversation diagram could be taken from
	the list of conversation partners,
	each with a list of incoming and outgoing messages,
	relative to the current engine family [family name].
	This is not yet implemented though.
	
## Guarded Actions

!!! note

	By default, guarded actions should be inlined in the same page. If an engine has
	too many guarded actions (and thereby putting them all in one page would be
	unworkable), they can be split out into separate files and linked.

??? todo

	ᚦ Put a link to the guarded action description/template,
	or how should we do this?


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
