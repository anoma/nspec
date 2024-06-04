# Protocol desiderata

## Intent machine

!!! todo

    describe basics of intent machine

## Heterogeneous trust

Suppose that program $P$ instantiates the Anoma protocol, and that an observer $O$ can interact with $P$ by sending and receiving messages (locally, in the sense that the interface is trusted). 

Assume that:
- The observer $O$ makes some _trust assumptions_ about how other agents $A_1, A_2, ... A_n$ will behave. These trust assumptions, for an agent $A$, are always of the form of a predicate over messages which $A$ is expected to send, possibly in response to messages they have received. For example, an assumption could be of the form that $A$ will never send two messages $M_1$ and $M_2$ such that, for some predicate $P$, $P(M_1, M_2) = 1$ (safety-related), or of the form that in response to receiving message $M$, $A$ will eventually respond with message $M'$, where, for some predicate $P$, $P(M, M') = 1$ (liveness-related). 

A valid implementation of Anoma must guarantee:
- _Consistency_: if _in fact_ $O$ is _correct_ about their trust assumptions, i.e. for each $A_n$ about which $O$ makes a trust assumption, $A_n$ does _in fact_ behave in the way in which $O$ assumes that they will, then for any other observer $O'$, if $O$ and $O'$ are both running program $P$, in response to an arbitrary query message $Q$, $P$ will respond to $O$ and $O'$ with the same response $R$.
- _Liveness_: if _in fact_ $O$ is _correct_ about their liveness-related trust assumptions, i.e. for each $A_n$ about which $O$ makes a trust assumption, $A_n$ does _in fact_ behave in the way in which $O$ assumes that they will, then for any other observer $O'$, if $O$ and $O'$ are both running program $P$, in response to an arbitrary input message $M$, $P$ will eventually respond to $O$ and $O'$. (note: $P$ needs to have the same private information)

imagine that we had an oracle?

## Information flow control

!!! todo

    orthogonality of information disclosure
    expression of preferences

## Model convergence

!!! todo

    convergence of distribution of state
    convergence of estimations