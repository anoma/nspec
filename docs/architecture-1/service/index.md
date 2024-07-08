---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Service Architecture

Basic promises:

- respond to messages under certain conditions (liveness)
- never send messages satisfying certain criteria (safety)

Kinds of services:

- ordering
- storage
- compute
- bandwidth


## Heterogeneous trust

Suppose that program $P$ instantiates the Anoma protocol, and that an observer $O$ can interact with $P$ by sending and receiving messages (locally, in the sense that the interface is trusted).

Assume that:

- The agent $A$ makes some _trust assumptions_ about how other agents $A_1, A_2, ... A_n$ will behave. These trust assumptions, for an agent $A$, are always of the form of a predicate over messages which $A$ is expected to send, possibly in response to messages they have received. For example, an assumption could be of the form that $A$ will never send two messages $M_1$ and $M_2$ such that, for some predicate $P$, $P(M_1, M_2) = 1$ (safety-related), or of the form that in response to receiving message $M$, $A$ will eventually respond with message $M'$, where, for some predicate $P$, $P(M, M') = 1$ (liveness-related).

A valid instantiation of Anoma must guarantee:

- _Consistency_: if _in fact_ $O$ is _correct_ about their trust assumptions, i.e. for each $A_n$ about which $O$ makes a trust assumption, $A_n$ does _in fact_ behave in the way in which $O$ assumes that they will, then for any other observer $O'$, if $O$ and $O'$ are both running program $P$, in response to an arbitrary query message $Q$, $P$ will respond to $O$ and $O'$ with the same response $R$.
- _Liveness_: if _in fact_ $O$ is _correct_ about their liveness-related trust assumptions, i.e. for each $A_n$ about which $O$ makes a trust assumption, $A_n$ does _in fact_ behave in the way in which $O$ assumes that they will, then for any other observer $O'$, if $O$ and $O'$ are both running program $P$, in response to an arbitrary input message $M$, $P$ will eventually respond to $O$ and $O'$. (note: $P$ needs to have the same private information)

## Information flow control

Suppose that program $P$ instantiates the Anoma protocol, and that an agent $A$ can interact with $P$ by sending and receiving messages locally.

Assume that:

- The agent $A$ makes some _trust assumptions_ about how other agents $A_1, A_2, ... A_n$ will behave. These trust assumptions, for an agent $A$, are always of the form of a predicate over messages which $A$ is expected to send, possibly in response to messages they have received. For example, an assumption could be of the form that, given that $A$ has received some message $M_1$, $A$ will never send a message $M_2$ such that, for some predicate $P$, $P(M_1, M_2) = 1$ (this could indicate, for example, that $M_2$ discloses some information in $M_1$).

A valid instantiation of Anoma must guarantee:

- _Bounded disclosure_: if $A$ discloses certain information $I$ to a set of parties $A_1 ... $A_n$, with instructions not to disclose it to further parties, and _in fact_ $A$ is _correct_ about their trust assumptions, i.e., for each $A_n$ about which $A$ makes a trust assumption, $A_n$ does _in fact_ behave in the way in which $A$ assumes that they will, for all agents $A'$ not in $A_1 ... A_n$, $A'$ will not learn the information as a result of $A$'s disclosure of it.
- _Orthogonal disclosure_: if $A$ knows certain information $I$, for an arbitrary function $F_I$, $A$ can disclose the result of $F_I$ to arbitrary other agents without disclosing anything else.
