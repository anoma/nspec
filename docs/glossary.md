# English Glossary


## How to use this Glossary

Since this specification is (for now at least) a work in progress, many sections
are still in flux. To make it easier to understand, as well as preserve
flexibility for refactoring, we strive to maintain this glossary as described
below:

### Introducing New Terminology

1. When introduction a new term, we list it here and link to the section of the
   spec containing its definition.
2. Once a section has become reasonably stable we add short explanations to the
   terms used in them.

### Using Existing Terminology

1. When using a term that has been defined elsewhere, we list it here and link
   to an external reference, which should captures the sense of our usage.
2. Once a section has become reasonably stable we add short excerpts to the
   citations.

An existing term should be included in the following cases (incomplete list):

- If it is central to the understanding of concepts in the spec.
- If it is hard to look up, e.g. different subfields have different definitions.
- If it is likely that the intended audience of the containing sections is unfamiliar with it.

## Collaborative Glossary Maintenance

To get the glossary into shape, its maintenance will have the following phases:

1. Section authors add terms introduced and used in their sections.
2. Reviewers point out omissions.

After a first pass of populating the glossary, the two phases will continue to
happen in parallel for a while.

Since the decision whether to include an existing term or not will be more of a
soft question, reviewer and reader feedback will be especially important.

# Definitions

## Anoma protocol

The Anoma protocol is the logical framework which [agents](#agent) use to read,
create, and process [messages](#message).

## Agent

An *agent* is a non-deterministic, stateful entity which can send and receive
messages.

The term "agent" is similar to "process" used in distributed systems. However,
"agent" is used to highlight the possibility of non-deterministic behaviour,
such as random events or choices made by external users. The term also
emphasizes the idea of decision-making that can affect the state of the system.
This is important for ensuring that the state of the system accurately reflects
the state of the world. To achieve this, individual agents must provide data
inputs that correspond in local ways, as the system protocol itself does not
have direct knowledge of the state of the world.

<!--
The concept of _agent_ is similar to that of _process_ as used in the distributed systems literature. We use "agent" to emphasize non-determinism (local randomness and/or external user choice input) and possible agency (in the sense of decision-making which impacts the state of the system).

The latter is especially important as *causal accounting* requires correspondence between the state of the system and state of the world, a correspondence which can only be maintained as a product of individual data inputs by agents which themselves correspond in local ways, as the protocol itself has no knowledge of the state of the world.
-->


## Canonical serialization

A *canonical serialization* refers to a standardized way of representing data or
functions as a series of bytes that can be transmitted across a network.

Canonical serialization are fully discussed in Primitives.

## Turing-equivalent

"Turing-equivalent" means that the functions and data being transmitted can be
computed by a Turing machine, a well-known theoretical model of computation.

## Message

A *message* is any datum sent between agents.

## State

A *state* may refer to the state of an agent, the state of the world, or the state of the system.

- The *state of an agent* is the set of all data stored by the agent.

- The *state of the system* is a function of the decisions taken by agents
over (partially ordered) time.

- The *state of the world* is the set of
data related to the "real world" that is observed by and of interest to the agents.

## System

A *system* is a virtual environment which
consists of a set of agents interacting with each other.
