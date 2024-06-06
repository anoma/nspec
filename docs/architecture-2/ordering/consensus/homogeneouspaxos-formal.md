---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Formal definition of WellFormed

## Assumption: homogenous case

We assume that the set of learners is a singleton, $\Learner = \cb{\red\alpha}$.

## Definition: Message Signer

$$
  \sig{\green x : \Message} \eqdef
  \textrm{the acceptor or proposer that signed } {\green x}
$$

## Definition: Message Set Signers

We extend $\sig{}$ over sets of messages, to mean the set of signers of those messages:

$$
  \sig{\green M : 2^{\Message}} \eqdef
  \cb{{\sig{\blue m}} \mid {\blue m \in \green M}}
$$

Messages contain a field $\refs$, which includes chained hashes of every message the sender has sent or received since (and including) the last message it sent.
Ballot proposals ($1a$-messages) do not reference other messages.

We define the transitive references of a message, which should include every message the sender has ever sent or received, as follows.

## Definition: Transitive References

$$
  \tran{\green x} \eqdef
  \cb{\green x} \cup \bigcup_{\blue m \in \green{x.\refs}} \tran{\blue m}
$$

We say that message $\red y$ is _visible_ from message $\green x$ if ${\red y} \in \tran{\green x}$.
<!--- acceptor $\red a$ is _visible_ from message $\green x$ if ${\red a} \in \sig{\tran{\green x}}$ -->

The algorithm requires that the received messages are processed in the order they were sent by any given sender.
In order to ensure this, the safe acceptors delays doing any computations on message $m$ until they have received all the messages in $m.\refs$.

Messages contain a field $\prev$, which stores a hash of the last message sent by the acceptor, if it exists. Otherwise, it stores a special non-hash value $\bot$.
Similarly to the definition above, we define transitive history of the messages sent by the acceptor.

## Definition: Transitive History

$$
  \prevtran{\green{x}} \eqdef
  \cb{\green x} \cup
  \begin{cases}
    \prevtran{\green{x.\prev}} &\text{ if } \green{x.\prev} \neq \bot \\
    \emptyset &\text{ otherwise}
  \end{cases}
$$

Clearly, for any message $\green x$ originating from a safe acceptor, the messages of $\prevtran{\green x}$ form a linear history chain with respect to $\prev$ field.

## Definition: Get1a

We define $1a$-message that started the ballot of the message as the highest ballot value $1a$-message visible from it.

$$
  \geta{\green x} \eqdef
  \argmax_{\blue m:\textit{1a} \in \tran{\green x}}{\blue{m.ballot}}
$$

Since every proposed ballot is unique, the function $\geta{}$ is well-defined.

## Definition: Ballot Numbers

The ballot number of the message is the highest ballot number among the visible $\onea$ messages.

$$
  \ba{\green x} \eqdef \geta{\green x}.ballot
$$

## Definition: Value of a Message

The value of a the message is the value of the highest ballot number among the visible $\onea$ messages.

$$
  \va{\green x} \eqdef \geta{\green x}.value
$$

Using the above auxiliary functions, we formally define decisions by

## Definition: Decision

For any set of messages $\blue{s}$ and ballot $b$

$$
  \Decision{\red\alpha}{b, \blue s} \eqdef
  \sig{\blue s} \in Q_{\red\alpha} \land
  \forall {\green x},{\purple y} \in {\blue s}.\,
    \vartype{\green x}{\twoa} \land
    \ba{\green x} = b
$$

<!-- HPaxos 2.0 definition -->
<!-- $$
  \Decision{\red\alpha}{\blue s} \eqdef
  \sig{\blue s} \in Q_{\red\alpha} \land
  \forall {\green x},{\purple y} \in {\blue s}.\,
    \vartype{\green x}{\twoa} \land
    {\red\alpha} \in \green{x.\mlearner} \land
    \ba{\green x} = \ba{\purple y}
$$ -->

To define what makes a _wellformed_ $\twoa$ message, it requires checking whether two learners might be entangled, and (unless we can prove they are not entangled), whether one of them might have already decided.

## Definition: Caught

Some behavior can create a proof that an acceptor is Byzantine.
Unlike Byzantine Paxos, our acceptors and learners must adapt to Byzantine behavior.
We say that an acceptor $\purple p$ is _caught_ in a message $\green x$ if the transitive references of $\green x$ include evidence such as two messages, $\red m$ and $\blue{m^\prime}$, both signed by $\purple p$, in which neither is featured in the other's transitive history chain.

$$
  \caughtEvidence{{\red m}, {\blue{m'}}} \eqdef
  \sig{\red m} = \sig{\blue{ m^\prime}} \land
  \red m \not\in \prevtran{\blue{m^\prime}} \land
  \blue{m^\prime} \not\in \prevtran{\red m}
$$

$$
  \caught{\green x} \eqdef
  \sig{\cb{{\red m} \in \tran{\green x} \mid \exists {\blue{m'}} \in \tran{\green x}.\,\caughtEvidence{{\green x}, {\red m}, {\blue{m'}}}}}
$$

**Caught proofs processing**: Caught evidences of misbehavior can be used, e.g., for the acceptor punishment, such as slashing in the context of proof-of-stake protection mechanism.

## Definition: Accurate _as of_ a Message $\green x$
When some acceptors are proved Byzantine, $\red\alpha$ may no longer be _accurate_, meaning its decisions no longer need to agree. 
This happens when the safe set of acceptors isn't in the learner's safe sets: $\reallysafe\not\in \red{safe_\alpha}$, i.e.
at least one acceptor in each safe set is proven Byzantine.
With the $\caught{}{}$ relation, we can talk about whether $\red \alpha$ can still be accurate as of a given message (as opposed to proven to be inaccurate): 

$$
  \textrm{Acc}\p{\green x} \eqdef
    \exists {\purple s} \in \red{safe_\alpha} .\,
    {\purple s} \cap \caught{\green x} = \emptyset
$$
<!-- HPaxos 2.0 definition -->
<!-- $$
  \con{\red \alpha}{\green x} \eqdef
  \cb{
    {\blue \beta} \in \Learner \mid
    \exists {\purple s} \in \edge{\red\alpha}{\blue\beta} \in \lgraph.\,
    {\purple s} \cap \caught{\green x} = \emptyset
  }
$$ -->

## Definition: Buried

A $\twoa$-message can become irrelevant if, after a time, an entire quorum of acceptors has seen $\twoa$s with different values, <!-- <span style="background-color: #E2E2FF">the same learner</span>, --> and higher ballot numbers.
We call such a $\twoa$ _buried_ (in the context of some later message $\green y$).

$$
  \burying{{\blue z}}{{\purple x}} \eqdef
  \vartype{\blue z}{\twoa} \land
  \ba{\blue z} > \ba{\green x} \land
  \va{\blue z} \ne \va{\green x}
$$

$$
  \buried{{\red\alpha}}{\vartype{\purple x}{\twoa}}{\green y} \eqdef
  \sig{\cb{
    {\orange m} \in \tran{\green y} \mid
    \exists {\blue z} \in \tran{\orange m}.\burying{\blue z}{\purple x}
  }}
  \in Q_{\red\alpha}
$$

We shall say that the message $\green x$ is _unburied_ (in the context of a later message $\purple y$) if it is not buried (in the context of $\purple y$).

## Definition: Connected 2a-messages
For learner $\red \alpha$, it can be useful to find the set of $\twoa$-messages from the same sender as a message ${\green x}$ (and sent earlier)
which are still [unburied](#definition-buried) and for learners connected to $\red \alpha$.
We call these 2as "connected" for reasons which make more sense in full heterogeneous paxos. 
If a message $\green x$ proves that $\red \alpha$ is not _accurate_, then it is in some sense not "bound" by earlier $\twoa$-messages: $\red \alpha$ can decide contradictory values. 

$$
  \cona{\hetdiff{\red\alpha}}{\green x} \eqdef
  \cb{
    \tallpipe
    {{\purple m} \in \tran{\green x}}
    {\begin{array}{l}
      \phantom{\land}\, \vartype{\purple m}{\twoa} \\
      \land\, {\sig{\purple m} = \sig{\green x}} \\
      \land\, \textrm{Acc}\p{\green x} \\
      \land\, \lnot \buried{\red\alpha}{\purple m}{\green x}
     \end{array}}
  }
$$
<!-- HPaxos 2.0 definition -->
<!-- $$
  \cona{\hetdiff{\red\alpha}}{\green x} \eqdef
  \cb{
    \tallpipe
    {{\purple m} \in \tran{\green x}}
    {\begin{array}{l}
      \phantom{\land}\, \vartype{\purple m}{\twoa} \\
      \land\, {\sig{\purple m} = \sig{\green x}} \\
      \land\, \exists \blue{\beta} \in \con{\red \alpha}{\green x}.\,
          \lnot \buried{\blue \beta}{\purple m}{\green x}
     \end{array}}
  }
$$ -->

## Definition: Fresh

Acceptors send a $\oneb$-message whenever they receive a $\onea$-message with a ballot number higher than they have yet seen.
However, this does not mean that the $\oneb$'s value (which is the same as the $\onea$'s) agrees with that of $\twoa$-messages the acceptor has already sent.
We call a $\oneb$-message _fresh_ (with respect to a learner) when its value agrees with that of unburied $\twoa$-messages the acceptor has sent.

$$
  \fresh{\hetdiff{\red \alpha}}{\green x : \oneb} \eqdef
  \forall \blue m \in \cona{\hetdiff{\red \alpha}}{\green x}.\, \va{\green x} = \va{\blue m}
$$

## Definition: Quorums in Messages

$\twoa$-messages reference _quorums of messages_ with the same value and ballot.
A $\twoa$'s quorums are formed from [fresh](#definition-fresh) $\oneb$-messages with the same ballot and value.

<!-- HPaxos 2.0 definition -->
<!-- $$
  \qa{\green x : \twoa} \eqdef
  \cb{\tallpipe
    {\red m \in \tran{\green x}}
    {{\red m : \oneb} \land
     {\fresh{\hetdiff{\green{x.lrn}}}{\red m}} \land
     {\ba{\red m} = \ba{\green x}}}
  }
$$ -->
$$
  \qa{\green x : \twoa} \eqdef
  \cb{\tallpipe
    {\red m \in \tran{\green x}}
    {{\red m : \oneb} \land
     {\fresh{\red\alpha}{\red m}} \land
     {\ba{\red m} = \ba{\green x}}}
  }
$$

## Definition: Chain property

$$
  \ChainRef({\green x}) \eqdef
    \green{x.\prev} \neq \bot \to
      \green{x.\prev} \in \green{x.\refs} \land
      \sig{\green{x.prev}} = \sig{\green x}
$$

## Definition: WellFormed

We define what it means for a message to be _wellformed_.

$$
  \begin{array}{l}
    \WellFormedOneB{\green x} \eqdef
    \forall \blue y \in \tran{\green x} .\,
    \green x \ne \blue y \land \blue y \ne \geta{\green x}
    \to \ba{\blue y} \ne \ba{\green x}
    \\
    \WellFormedTwoA{\green x} \eqdef
    \qa{\green x} \in \green{Q_{\red{\alpha}}}
    \\
    \wellformed{\green x} \eqdef \\
    \qquad
    \phantom{\land}\, \ChainRef({\green x})
    \\ \qquad
    \land\, \p{\vartype{\green x}{\oneb} \to (\exists {\red z} \in \green{x.\refs}.\,\vartype{\red z}{\onea}) \land \WellFormedOneB{\green x}}
    \\ \qquad
    \land\, \p{\vartype{\green x}{\twoa} \to {\green x}.\refs \neq \emptyset \land \WellFormedTwoA{\green x}}
  \end{array}
$$
