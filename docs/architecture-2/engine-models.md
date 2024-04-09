# Engine Models

Engines communicate via message passing.
Each _message_ consists of a header and a body.
The _header_ gives information about the sender and the intended destination,
e.g., in the form of ɪᴅs or addresses.
The type of the _body_ almost always depends on the specific type of message.
For each engine,
we provide the following.

1. _A list of type **names**_
   Each _type name_ is a string that specifies
   the type of message bodies that the engine has to be able to process
   (with the additional context that the header provides). <!--
   Type names are also used for naming the places in the Petri net model.
   -->
   Optionally,
   each type name in this list is mapped to a set of protocols to which it belongs.
2. _A list of pairs of type names and engines for message reactions_
   Each type name has a “static” approximation of all message reactions
   that a received message might trigger.
   Typically, there is no need to add identities or addresses of engine instance here.
3. _A type for each type name_
   The type of the message body is called _message type_ as short hand for _message body type_.
   The message type does not need to re-iterate information of the message header.
   It is allowed that several type names refer to the message type.

4. _The types and behavior for each message body type_
   Using links to github,
   Message types should be specified as
   [color sets](https://cpntools.org/2018/01/12/color-sets/)
   or as rust types as a fallback option,
   ideally both.
   The behavior also has to give some information about headers,
   and define the behavior,
   using SML functions.

   <!--
   If possible,
   we describe the behavior in terms of messages previously received.
   This could be achieved by sending auxiliary messages to “self” (bypassing the network),
   effectively calling “self” with a new message.

   The behavior should be specified as
   [SML functions](https://cpntools.org/2018/01/09/functions-declarations-and-control-structures/)
   for [code segments](https://cpntools.org/2018/01/09/code-segments/)
   combined with [guards](https://cpntools.org/2018/01/09/guards/) that state pre-conditions
   in the sense of [Hoare triples](https://en.wikipedia.org/wiki/Hoare_logic#Hoare_triple),
   in particular to allow for several instances of the same engine.
   -->

Thus, the structure of the description of engine models is as follows.

- Engine 1
  _[…]_
- Engine 2
  _[…]_
- ⋮
- Engine $i$
  - MessageTypeName_$i_1$ [$\scriptscriptstyle\{<\mathrm{protocols}(i,1)>\}$]
    _<↑link to github repo`MessageType_i_1`>_
    _[…]_
  - ⋮
  - MessageTypeName_$i_j$ [$\scriptscriptstyle\{<\mathrm{protocols}(i,j)>\}$]
    _<↑link to github repo`MessageType_i_j`>_
    - ReactionTypeName_$p_{i,j,1}$ → Engine_$q_{i,j,1}$
      _<one liner i,j,1>_
    - ReactionTypeName_$p_{i,j,2}$ → Engine_$q_{i,j,2}$
      _<one liner i,j,2>_
    - ⋮
    - ReactionTypeName_$p_{i,j,k}$ → Engine_$q_{i,j,k}$
      _<one liner i,j,k>_
    - ⋮
    - ReactionTypeName_$p_{i,j,m_{i,j}}$ → Engine_$q_{i,j,m_{i,j}}$
      _<one liner i,j,m_{i,j}>_
  - ⋮
  - MessageTypeName_$i_{m_i}$ [$\scriptscriptstyle\{<\mathrm{protocols}(i,m_i)>\}$]
    _<↑link to github repo`MessageType_i_{m_i}`>_
    _[…]_
- ⋮
- engine $N$
