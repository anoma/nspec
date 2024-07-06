---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Serialisation

The protocol requires a [*canonical* serialisation](../glossary.md#canonical-serialization) of [Turing-equivalent](../glossary.md#turing-equivalent) functions and data.

A *serialisation* can be any function which maps data to a series of bytes. The inverse function which maps a series of bytes to data is referred to as a *deserialisation*.

Being *canonical* for a serialisation $s$ means that there exists a function $d$
such that, for any function or data $x$, all the agents using the protocol agree
that the following equation holds.

$$s(\mathsf{eval}(d(x))) = x.$$

In what follows, we assume any serialisation is canonical, unless otherwise specified. Internal representations of compute may vary as long as this external equivalence holds. Certain additional correspondences of internal representations may be required for particular verifiable computation schemes (see below).

For the remainder of this specification, this canonical representation is taken as implicit, and may be assumed where appropriate (e.g. `serialise` is called before sending a function over the network).