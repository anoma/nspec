---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Formal definition of WellFormed

## Definition: Message Signer

$$
  \sig{\green x : \Message} \triangleq
  \textrm{the acceptor or proposer that signed } {\green x}
$$

## Definition: Message Set Signers

We extend $\sig{}$ over sets of messages, to mean the set of signers of those messages:

$$
  \sig{\green M : 2^{\Message}} \triangleq
  \cb{{\sig{\blue m}} \mid {\blue m \in \green M}}
$$

Messages contain a field $\refs$, which includes chained hashes of every message the sender has sent or received since (and including) the last message it sent.
Ballot proposals ($1a$-messages) do not reference other messages.

We define the transitive references of a message, which should include every message the sender has ever sent or received, as follows.

## Definition: Transitive References

$$
  \tran{\green x} \triangleq
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
  \prevtran{\green x} \triangleq \cb{\green x} \cup \prevtran{\green x.\prev}
$$

Clearly, for any message $\green x$ originating from a safe acceptor, the messages of $\prevtran{\green x}$ form a linear history chain with respect to $\prev$ field.

## Definition: Get1a

We define $1a$-message that started the ballot of the message as the highest ballot value $1a$-message visible from it.

$$
  \geta{\green x} \triangleq
  \argmax_{\blue m:\textit{1a} \in \tran{\green x}}{\blue{m.ballot}}
$$

Since every proposed ballot is unique, the function $\geta{}$ is well-defined.

## Definition: Ballot Numbers

The ballot number of the message is the highest ballot number among the visible $1a$s.
$$
  \ba{\green x} \triangleq \geta{\green x}.ballot
$$

## Definition: Value of a Message

The value of a the message is the value of the highest ballot number among the visible $1a$s.

$$
  \va{\green x} \triangleq \geta{\green x}.value
$$

Using the above auxiliary functions, we formally define decisions by

## Definition: Decision

$$
  \decision{\red \alpha}{b, \red{q_\alpha}} \triangleq
  \sig{\red{q_\alpha}} \in \red{Q_\alpha} \land
  \forall \green x \in \red{q_\alpha}.\,
    \green x:\twoa \land
    \ba{\green x} = b \land
    \green{x.lrn} = {\red \alpha}
$$

To define what makes a _wellformed_ $\twoa$ message, it requires checking whether two learners might be entangled, and (unless we can prove they are not entangled), whether one of them might have already decided.

## Definition: Caught

Some behavior can create a proof that an acceptor is Byzantine.
Unlike Byzantine Paxos, our acceptors and learners must adapt to Byzantine behavior.
We say that an acceptor $\purple p$ is _caught_ in a message $\green x$ if the transitive references of $\green x$ include evidence such as two messages, $\red m$ and $\blue{m^\prime}$, both signed by $\purple p$, in which neither is featured in the other's transitive history chain.

$$
  \caughtEvidence{{\red m}, {\blue{m'}}} \triangleq
  \sig{\red m} = \sig{\blue{ m^\prime}} \land
  \red m \not\in \prevtran{\blue{m^\prime}} \land
  \blue{m^\prime} \not\in \prevtran{\red m}
$$

$$
  \caught{\green x} \triangleq
  \sig{\cb{{\red m} \in \tran{\green x} \mid \exists {\blue{m'}} \in \tran{\green x}.\,\caughtEvidence{{\green x}, {\red m}, {\blue{m'}}}}}
$$

**Caught proofs processing**: Caught evidences of misbehavior can be used, e.g., for the acceptor punishment, such as slashing in the context of proof-of-stake protection mechanism.

## Definition: Connected

When some acceptors are proved Byzantine, some learners need not agree,
meaning that any safe set of acceptors $\reallysafe$ isn't in the edge between them in the learner graph $\lgraph$, i.e.,
at least one acceptor in each safe set in the edge is proven Byzantine.
Homogeneous learners are always connected unless there are so many failures no consensus is required.

$$
  \con{\red \alpha}{\green x} \triangleq
  \cb{
    {\blue \beta} \in \Learner \mid
    \exists {\purple s} \in \edge{\red \alpha}{\blue \beta} \in \lgraph.\,
    {\purple s} \cap \caught{\green x} = \emptyset
  }
$$

## Definition: Buried

A $\twoa$-message can become irrelevant if, after a time, an entire quorum of acceptors has seen $\twoa$s with different values,
<span style="background-color: #E2E2FF">the same learner</span>, and higher ballot numbers.
We call such a $\twoa$ _buried_ (in the context of some later message $\purple y$).

$$
  \burying{{\blue z}}{{\green x} : \twoa} \triangleq
  z:\twoa \land
  \ba{\blue z} > \ba{\green x} \land
  \va{\blue z} \ne \va{\green x} \land
  \hetdiff{\blue{z.lrn} = \green{x.lrn}}
$$

$$
  \buried{\green x : \twoa}{\purple y} \triangleq
  \sig{\cb{
    {\red m} \in \tran{\purple y} \mid
    \exists {\blue z} \in \tran{\red m}.\, \burying{\blue z}{\green x}
  }}
  \in \green{Q_{\hetdiff{x.lrn}}}
$$

We shall say that the message $\green x$ is _unburied_ (in the context of a later message $\purple y$) if it is not buried (in the context of $\purple y$).

## Definition: Connected $\twoa$-messages

Entangled learners must agree, but learners that are not connected are not entangled, so they need not agree.
Intuitively, a $\oneb$-message references a $\twoa$-message to demonstrate that some learner may have decided some value.
For learner $\red \alpha$, it can be useful to find the set of $\twoa$-messages from the same sender as a message ${\green x}$ (and sent earlier)
which are still [unburied](#definition-buried) and for learners connected to $\red \alpha$.
The $\oneb$ cannot be used to make any new $\twoa$-messages for learner $\red \alpha$ that have values different from these $\twoa$-messages.

<!-- $$
  \cona{\hetdiff{\red \alpha}}{\green x} \triangleq
  \cb{
    {\blue m} \in \tran{\green x} \mid
    {\blue m : \twoa} \land
    {\sig{\blue m} = \sig{\green x}} \land
    {\lnot \buried{\blue m}{\green x}} \land
    {\hetdiff{\blue{m.lrn} \in \con{\red \alpha}{\green x}}}
  }
$$ -->

$$
  \cona{\hetdiff{\red \alpha}}{\green x} \triangleq
  \cb{
    \tallpipe
    {{\blue m} \in \tran{\green x}}
    {\andlinesFour
      {\blue m : \textit{2a}}
      {\sig{\blue m} = \sig{\green x}}
      {\lnot \buried{\blue m}{\green x}}
      {\hetdiff{\blue{m.lrn} \in \con{\red \alpha}{\green x}}}
  }}
$$

## Definition: Fresh

Acceptors send a $\oneb$-message whenever they receive a $\onea$-message with a ballot number higher than they have yet seen.
However, this does not mean that the $\oneb$'s value (which is the same as the $\onea$'s) agrees with that of $\twoa$-messages the acceptor has already sent.
We call a $\oneb$-message _fresh_ (with respect to a learner) when its value agrees with that of unburied $\twoa$-messages the acceptor has sent.

$$
  \fresh{\hetdiff{\red \alpha}}{\green x : \oneb} \triangleq
  \forall \blue m \in \cona{\hetdiff{\red \alpha}}{\green x}.\, \va{\green x} = \va{\blue m}
$$

## Definition: Quorums in Messages

$\twoa$-messages reference _quorums of messages_ with the same value and ballot.
A $\twoa$'s quorums are formed from [fresh](#definition-fresh) $\oneb$-messages with the same ballot and value.

$$
  \qa{\green x : \twoa} \triangleq
  \cb{\tallpipe
    {\red m \in \tran{\green x}}
    {{\red m : \oneb} \land
     {\fresh{\hetdiff{\green{x.lrn}}}{\red m}} \land
     {\ba{\red m} = \ba{\green x}}}
  }
$$

## Definition: WellFormed

We define what it means for a message to be _wellformed_.
$$
  \begin{array}{l}
    \wellformed{\purple u : \onea} \triangleq
    {\purple u}.\refs = \emptyset
    \\
    \wellformed{\green x : \oneb} \triangleq
    {\green x}.\refs \ne \emptyset
    \land
    \forall \blue y \in \tran{\green x} .\,
      \green x \ne \blue y
      \land
      \blue y \ne \geta{\green x}
      \Rightarrow
      \ba{\blue y} \ne \ba{\green x}
    \\
    \wellformed{\red z : \twoa} \triangleq
    {\red z}.\refs \ne \emptyset
    \land
    \sig{\qa{\red z}} \in \red{Q_{\hetdiff{z.lrn}}}
\end{array}
$$
