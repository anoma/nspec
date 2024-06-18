---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Proof-of-stake

This section describes an example of a simplified version of the Proof-of-Stake application. The goal of the PoS protocol is to assign voting power in the BFT consensus algorithm: users delegate their tokens to validators, the voting power of each validator is determined from the amount of tokens delegated to them. The delegated tokens are locked for a period of time, so that if the validator misbehaves, this behaviour could be tracked and reacted on by burning a part of the delegated tokens. This application can be a useful building block for other applications or, more generally, for the contexts that require a decision-making mechanism.

## Roles

|Role|Description|
|-|-|
|User|The party that delegates tokens to validators, expressing a certain degree of agreement with the decisions the validator makes on the user's behalf.|
|Pool|The account that stores (owns) delegated tokens. Can be implemented with a generic account resource kind|
|Validator|The party that participates in the consensus algorithm, voting for decisions. The voting power is determined by how much token the users delegate to the validator.|


## Resource kinds

|Resource kind|Description|Create|Consume|
|-|-|-|-|
|Token|Governance token used to distribute the voting power|Generic token logic|Generic token logic|
|Pool|Special type of the token owner account that owns all bonds|Generic account logic|Generic account logic|
|Bond|Represents a bonded token delegated to a validator. Always owned by the pool|Requires the user to send their assets to the pool |Can be consumed to create a withdrawal.
|Withdrawal|Represents the asset in the process of undelegation|Created from a bond| Can be consumed when the portion of assets remaining after the slashing is performed is sent from the pool to the user, strictly after $W_{unlock}$
|Infraction|Represents a proof of misbehaviour of a certain validator |Created provided a proof of misbehaviour| Never consumed
|Voting power|Contains the distribution of voting power among the validators|Can be created provided a proof of correct computation of voting power from the existing bonds| Never consumed

### Bond

|Field|Description|
|-|-|
|$B_{quantity}$| How much token is bonded. Used to determine the voting power|
|$B_{validator}$| Refers to the validator the token is delegated to
|$B_{owner}$| Refers to the delegator

#### Bond logic

- Create:
    - Verify $T$ kind to be the governance token kind (for both the created and consumed resource)
    - A token resource $T$ was transferred from $T_{owner}$ to the pool:
        - Consumed token resource belonged to $T_{owner}$
        - Created token resource belongs to the pool
        - $T_{quantity}^{consumed} = T_{quantity}^{created}$
    - $B_{quantity}$ = $T_{quantity}$
    - $B_{owner}$ = $T_{owner}$

- Consume:
    - A withdrawal of kind $W$ is consumed
        - Verify $W$ kind

### Withdrawal

|Field|Description|
|-|-|
|$W_{validator}$| refers to the validator the token is delegated to
|$W_{owner}$| refers to the delegator
|$W_{unlock}$| defines the time after which the resource can be consumed

#### Withdrawal logic
- Create:
    - A bond of kind $B$ is consumed
        - Verify $B$ kind
    - $W_{quantity} = B_{quantity}$
    - $W_{validator} = B_{validator}$
    - $W_{owner}$ = $B_{owner}$
    - $W_{unlock} = now + U$, where $U$ is a constant value

- Consume:
    - Verify $T$ kind to be the governance token kind (for both the created and consumed resource)
    - A token resource $T$ was transferred from the pool to $W_{owner}$:
        - Consumed token resource belonged to the pool
        - Created token resource belongs to $W_{owner}$
        - $T_{quantity}^{consumed} = T_{quantity}^{created}$
    - $T_{quantity}$ = $W_{quantity}*\Pi{(1 - I_{rate})}$, where $I_{rate}$ is the infraction rate of infraction $I$ associated with this validator (iterate over all infractions created between the delegation and $W_{unlock}$ time)
    - $W_{owner}$ = $T_{owner}$

### Infraction

|Field|Description|
|-|-|
|$I_{validator}$| committed the misbehaviour
|$I_{rate}$| infraction rate determines how much to slash
|$I_{timestamp}$| defines when the misbehaviour was committed

#### Infraction logic
- Create:
    - Verify a proof of misbehaviour of the validator $I_{validator}$ at $I_{timestamp}$
- Consume:
    - Never

### VotingPower
|Field|Description|
|-|-|
|$VP_{map}$| contains a map between validators and their current voting power
|$VP_{timestamp}$| defines the time period for which the voting power is computed

#### VotingPower logic
- Create:
    - Provided with all bonds (read data, not consumed), iterate over them and compute the voting power for each validator: $VP_{map}[V] = \Sigma_{B_{validator} = V}{B_{quantity}}$
- Consume:
    - Never

## PoS application

### Application logic

$l_{PoS} = \{l_{Token}, l_{Pool}, l_{Bond}, l_{Withdrawal}, l_{Infraction}, l_{VotingPower}\}$

### Application interface

1. **Delegate:** Transfer the token from $T_{owner}$ to the pool, create a `Bond` resource.
2. **Undelegate:** Consume a `Bond` resource, create a `Withdrawal` resource.
3. **Withdraw:** Consume a `Withdrawal` resource, transfer the corresponding token (accounting for the relevant infractions) from the pool to $W_{owner}$.
4. **Slash:** Create a `Infraction` resource provided a proof of misbehaviour.
5. **Calculate voting power:** Create a `VotingPower` resource with $VP_{timestamp} = now$.

<figure markdown="span">
![image](/docs/images/pos_interface.svg){ width="450" }
<figcaption markdown="span">
The interface provided by the proof-of-stake application
</figcaption>
</figure>
