# World model

Anoma operates with the fundamental conceptual frame of *agents* in a *world* who may often seek to share their observations of the world, pool their storage and computational resources, and coordinate their actions taken within the world for mutually preferred effect.

## Agents

*Agent* is a primary notion that aims to unify the notions of _process_ in the distributed systems literature, _organism_ in the theoretical biology literature (e.g. active inference), and the _subject of experience_ as articulated by Kant.

An *agent* is a _corporeal being_ possessed of _memory_, the ability to perform _computation_, internal _unity_, and _transcendental freedom_. To spell out each of these in turn:

- An agent is a _corporeal being_ in the sense of being possessed of a physical form and a boundary which delineates that which is part of the agent from that which is not. That which is not the agent is the world. That which is part of the agent is not revealed to the world except through messages sent outwards.
- An agent is possessed of _memory_ which can store the agent's own history of experience, computations derived from it, or any other data.
- An agent is possessed of the ability to perform arbitrary _computation_. For the time being, we assume that this computation is classical in nature, but the notion could be extended to quantum computation in the future.
- An agent is possessed of internal _unity_, in the sense that whatever parts compose the agent act in unison and may be modelled both internally and externally as a unified whole.
- An agent is possessed of _transcendental freedom_ in the Kantian sense, in that the agent can originate an action purely from itself, and that in response to certain inputs, the agent can always do otherwise. We furthermore assume that this self-origination of action is sufficient to provide a _random oracle_ whose output is not predictable.

In general, Anoma does _not_ assume that agent identity is fixed and temporally invariant. Agents may split themselves, merge with or absorb other agents, or otherwise alter their boundaries continuously. However, reasoning about the evolution of the system over time will require the assumption that the information known to the agents at the start of the period in question is in some form preserved.

Agents may be composed of many parts which may be variously of physical or biological natures. Roughly, Anoma understands the identity of an agent on the basis of unity of corporeality, memory, computation, and freedom of action. For example, a person and their smartphone or personal computer held in hand would together comprise a singular agent in the sense defined here, while two separate people or a person and a computer across the world would not.

## World

An agent always exists in a _world_. The _world_, in some sense, is simply the sum totality of that which is not the agent. The world, we assume, is generally of interest to agents: they may seek information from it, send information into it, depend on physical resources from it for their continued survival, and simply care about it for transcendental reasons of their own. It is only through the world that one agent can communicate with another, and the distinction in the identity of the other from the rest of the world must simply be inferred.

### Observations & actions

Agents can interact with the world in two ways: by taking _observations_ of it, and by performing _actions_ within it. _Observations_ can be understood as messages received from the world, while _actions_ can be understood as messages sent to it. 

_Observations_ may be directed by a particular conceptualization of phenomena, in which case they are called _measurements_, and accompanied by a name of semantic significance to the agent taking the measurement, or undirected, in which case they are called _perceptions_ and unaccompanied. Observations may be initiated by the agent itself or initiated by the world.

!!! note

      For example, an observation might be $12988388$.


!!! note

      For example, a measurement might be $(temperature, 25.5)$.

_Actions_, similarly, may be directed by a particular conceptualization of the agent-world boundary, in which case they are accompanied by a name of semantic significance to the agent taking the action, or undirected, in which case they are unaccompanied.

!!! note

      For example, a directed action might be $(set-thermostat, 22)$.

!!! note

      For example, an undirected action might be $23123412$.

### Causal structure

In general, the world which the agents inhabit is assumed to have _causal structure_ which is unknown but _connected_ and _agent-invariant_, i.e.:

- The world is _connected_: for at least some actions, the probability distribution of at least one other agent's future observations, conditioned on an agent's action, is not equal to the probability distribution not so conditioned. In other words, we assume that actions have effects. In a world where this does not hold, coordination would be pointless.
- The world is _agent-invariant_:
      - Agents observing the world in the _same way_ (the definition of this is left a bit vague, but suppose e.g. measuring the temperature at the same time in the same place) will receive the same result.
      - Agents taking actions in the _same way_ (the definition of this is left a bit vague, but suppose e.g. setting the same thermostat to the same level) will result in the same effects.

In order for the agents to build up a model of the behaviour of the world over time which will be useful in predicting the results of future actions, the world's causal structure must also be invariant under spatial and temporal translation (as, say, the known laws of physics are).

## Cybernetic agency

We assume that the world is _of interest_ to agents. (...) In general, agents may be interested in choosing their actions in such a manner as to regulate the probability distribution of their future observations, the probability distributions of future observations of other agents, and in general the probability distribution of inferred latent state of the world.

!!! todo

      Cybernetic agency is ... blahblah

!!! todo

      Is cybernetics really the right word here? Can we pin this down more mathematically?

!!! todo

      Diagram of the cybernetic loop.

## Coordination

- Observation-sharing for improved inference
- Memory sharing
- Compututation sharing
- Causal interdependence of actions
- Protocol to send messages around, agree on what to do


!!! todo

      Bit on compositional cybernetic agency.

!!! todo

      Anoma is one such protocol. Figure out the comparison to natural language. Is there an "ideal" such protocol in certain ways? Can we come up with a mathematical definition here? Can this be related to Brandom on discursive commitments?


What does composition mean?
- Insofar as objective is shared, act as one agent.

What is a protocol in this context?
- Way to automatically respond to messages


!!! todo

      Cleanup / reorganize / remove the rest of this old content.

## Agents

The Anoma architecture operates on the basis of *agents*. The architecture does not presume any sort of global view or global time. It also does not presume any particular _motivations_ of agents, but rather describes the state of the system as a function of the decisions taken by agents over (partially ordered) time. 

1. *Agent* is a primary notion in the Anoma protocol that aims to extend/replace
   the notion of _process_ in the distributed systems literature.

2. _Agents_ are assumed to have the ability to:
    - generate local randomness, 
    - locally store and retrieve data, 
    - perform arbitrary classical computations, 
    - create, send, receive and read messages over an
        arbitrary, asynchronous physical network.
   
2. Agents _may_ have local input (e.g. human user input) and/or local randomness
   (e.g. from a hardware random number generator).

3. Agents can _join_ and _leave_ the system at any
   time.

4. All *actions* committed by agents are recorded in the *history*. To commit an action is to send a message. The *state* of the system at any point in time is a function of the history of messages sent by agents up to that point in time.

## World

*Agents* are presumed to exist in a *world* which is not directly accessible to the protocol itself but which is of interest to agents.

1. Agents can take *measurements* of data in this world, to which they may attach *semantics* (local names). Measurements can be understood as messages received from the world.

> For example, a measurement might be: $$("temperature", 25.5)$$

2. Agents may take *actions* in this world, to which they may similarly attach semantics. Actions can be understood as messages sent to the world.

> For example, an action might be: $$("set\_thermostat", 22)$$

3. In general, this world which the agents inhabit is assumed to have _causal structure_ which is _unknown_ but _connected_ and _consistent_, in that:


4. Agents may have *preferences* about this world. In general, the preferences of agents range over the configuration space of their future possible observations. Preferences take a partial order. Agents' preferences may range not only over their own future observations but also over future observations of other agents which they know.

> For example, a preference indicating that an agent prefers a higher temperature might be: $$("temperature", 25) > ("temperature", 24)$$

5. Anoma does not presume any _a priori_ agreement on semantics, units of measurement, data of interest, means of measurement, capabilities of agents, actions possible to take, knowledge of conditional probability distributions, etc.

In general, Anoma aims to allow these agents to infer the underlying causal structure of this world and coordinate their actions within it to better satisfy their preferences. The rest of this specification defines the _Anoma protocol_, which is specific logic that agents run to read, create, and process messages. For convenience, the Anoma protocol shall be referred to henceforth as just _the protocol_.