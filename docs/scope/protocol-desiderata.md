---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Protocol desiderata

What is the flow from world model to desiderata?
- Different permissions (action-capacities) in the world
- Model these (e.g. linear resources)
- Promise some correspondence
    - Transfer you a sandwich
- Agree on changes to the database
    - Propagate to changes to the world

## Intent machine

!!! todo

    Describe basics of intent machine


## Heterogeneous trust

Suppose that program $P$ instantiates the Anoma protocol, and that an observer $O$ can interact with $P$ by sending and receiving messages (locally, in the sense that the interface is trusted).

Assume that:
- The observer $O$ makes some _trust assumptions_ about how other agents $A_1, A_2, ... A_n$ will behave. These trust assumptions, for an agent $A$, are always of the form of a predicate over messages which $A$ is expected to send, possibly in response to messages they have received. For example, an assumption could be of the form that $A$ will never send two messages $M_1$ and $M_2$ such that, for some predicate $P$, $P(M_1, M_2) = 1$ (safety-related), or of the form that in response to receiving message $M$, $A$ will eventually respond with message $M'$, where, for some predicate $P$, $P(M, M') = 1$ (liveness-related).

A valid implementation of Anoma must guarantee:
- _Consistency_: if _in fact_ $O$ is _correct_ about their trust assumptions, i.e. for each $A_n$ about which $O$ makes a trust assumption, $A_n$ does _in fact_ behave in the way in which $O$ assumes that they will, then for any other observer $O'$, if $O$ and $O'$ are both running program $P$, in response to an arbitrary query message $Q$, $P$ will respond to $O$ and $O'$ with the same response $R$.
- _Liveness_: if _in fact_ $O$ is _correct_ about their liveness-related trust assumptions, i.e. for each $A_n$ about which $O$ makes a trust assumption, $A_n$ does _in fact_ behave in the way in which $O$ assumes that they will, then for any other observer $O'$, if $O$ and $O'$ are both running program $P$, in response to an arbitrary input message $M$, $P$ will eventually respond to $O$ and $O'$. (note: $P$ needs to have the same private information)

imagine that we had an oracle?

## Information flow control

- Participants know some information
- Disclose information about that information
- Reason about transitive disclosure
- Bound transitive disclosure subject to trust assumptions

!!! todo

    Orthogonality of information disclosure
    Restriction to expressed preferences under trust assumptions

## Model convergence

!!! todo

    Convergence of distribution of state
    Convergence of estimations


!!! todo

    Imagine an omniscient observer who can see all messages and all private information.