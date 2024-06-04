# World model

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
      - The probability distribution of each agent's future observations, conditioned on another agent's action, is not equal to the probability distribution not so conditioned - in other words, we assume that actions have effects. In a world where this does not hold, coordination would be pointless.
      - The world _does not discriminate on the basis of agent identity_.
         - Agents taking measurements in the _same way_ (the definition of this is left a bit vague, but suppose e.g. measuring the temperature at the same time in the same place) will receive the same result, within some error epsilon.
         - Agents taking action in the _same way_ (the definition of this is left a bit vague, but suppose e.g. setting the same thermostat to the same level) will result in the same effects, within some error epsilon.

4. Agents may have *preferences* about this world. In general, the preferences of agents range over the configuration space of their future possible observations. Preferences take a partial order. Agents' preferences may range not only over their own future observations but also over future observations of other agents which they know.

> For example, a preference indicating that an agent prefers a higher temperature might be: $$("temperature", 25) > ("temperature", 24)$$

5. Anoma does not presume any _a priori_ agreement on semantics, units of measurement, data of interest, means of measurement, capabilities of agents, actions possible to take, knowledge of conditional probability distributions, etc.

In general, Anoma aims to allow these agents to infer the underlying causal structure of this world and coordinate their actions within it to better satisfy their preferences. The rest of this specification defines the _Anoma protocol_, which is specific logic that agents run to read, create, and process messages. For convenience, the Anoma protocol shall be referred to henceforth as just _the protocol_.