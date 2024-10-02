---
icon: material/graph
search:
  exclude: false
  boost: 2
---

# Introduction
​
The operational architecture specification concerns the state evolution of Anoma instances, broken into smaller steps: which messages are exchanged, how computation is performed on the level of function calls, and which intermediate states are reachable.
The specification is organized into the following sections:

- [Hardware Abstraction Machine](./hardware_abstraction/index.md)

- [Identity Machine](./identity/index.md)

- [Networking Machine](./networking/index.md)

- [[Ordering Machine]]

## Engine models

All engines communicate via message passing, following the paradigm of message
passing concurrency. Thus, the only direct state manipulations that engine
instances can perform are local state changes.

<!-- (In a sense, there is no such thing as **the** _global state_ of a chain, but only local views). -->

All instances of a specific kind of engine share their _behaviour_, which is
defined as a function that

- takes a message and the current local state of an engine instance as input and

- computes the set of new messages (to be sent to other engine instances as
  reaction to the received message) and, optionally, a state update.

By default, the local state of an engine instance is a (subset of) all messages
that are sent and received.

**On Engine Models**

Engines communicate via message passing. Each _message_ consists of a header and
a body. The _header_ gives information about the sender and the intended
destination, e.g., in the form of ɪᴅs or addresses. The type of the _body_
almost always depends on the specific type of message. For each engine, we
provide the following.

- _A list of type **names**_. Each _type name_ is a string that specifies
   the type of message bodies that the engine has to be able to process
   (with the additional context that the header provides).
    <!--
   Type names are also used for naming the places in the Petri net model.
   -->
   Optionally,
   each type name in this list is mapped to a set of protocols to which it belongs.

- _A list of pairs of type names and engines for message reactions_.  Each type
   name has a “static” approximation of all message reactions that a received
   message might trigger. Typically, there is no need to add identities or
   addresses of engine instance here.

-  _A type for each type name_. The type of the message body is called _message
   type_ as short hand for _message body type_. The message type does not need
   to re-iterate information of the message header. It is allowed that several
   type names refer to the message type.

- _The types and behaviour for each message body type_.  Using links to GitHub,
   Message types should be specified as SML types/datatypes (eventually matching
   the restrictions of [colorsets](https://cpntools.org/2018/01/12/color-sets/)
   of CPN Tools, i.e., only datatypes without proper recursion / induction). The
   behaviour also has to give some information about headers, and define the
   behaviour, using SML functions. This amounts to one function
   `ReactionTypeName_`$p_{i,j,1}$ as below.

   <!--
   If possible,
   we describe the behaviour in terms of messages previously received.
   This could be achieved by sending auxiliary messages to “self” (bypassing the network),
   effectively calling “self” with a new message.

   The behaviour should be specified as
   [SML functions](https://cpntools.org/2018/01/09/functions-declarations-and-control-structures/)
   for [code segments](https://cpntools.org/2018/01/09/code-segments/)
   combined with [guards](https://cpntools.org/2018/01/09/guards/) that state pre-conditions
   in the sense of [Hoare triples](https://en.wikipedia.org/wiki/Hoare_logic#Hoare_triple),
   in particular to allow for several instances of the same engine.
   -->

!!! todo

    Even when the following renders, it is not really clear what the structure of the description is.


![Message Diagram](transaction_flow.svg)
