---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Nockma
Nockma (Nock-Anoma) is a modification of the [Nock4K specification](https://docs.urbit.org/language/nock/reference/definition) and a Nock standard library altered and extended for use with Anoma. Nockma is designed to support the [transaction function interpreter requirements](./transaction_function.md#transaction-function), namely, global storage read and deterministic bounded computation costs.

Nockma is parameterized over a specific finite field $\mathbb{F}_h$ and function $h$. The function $h$ takes an arbitrary noun (a data unit in Nockma) as input and returns an element of $\mathbb{F}_h$. This function is used for verifying reads from content-addressed storage.

A **scry** (inspired by Urbit’s concept of the same name) is a read-only request to Anoma’s global content-addressed namespace or indices computed over values stored in this namespace. Scrying is used to read data that would be inefficient to store in the noun, to read indices whose value might only be known at execution time, or to read data that may not be accessible to the author of the noun.

Scrying comes in two types: "direct" or "index". A direct lookup simply returns the value stored at the address (integrity can be checked using $h$), or an error if a value is not found. An index lookup uses the value stored at the address as an index function and returns the results of computing that index or an error if the index is not found, invalid, or uncomputable. The lookup type is the only parameter required apart from the content address (which must be an element of $\mathbb{F}_h$).

Typically, the index functions allowed will be very restricted, e.g. current unspent resources of a particular kind. Gas costs of scrying will depend on the index function and the size of the results returned.

Scrying may be used to avoid unnecessary, redundant transmission of common Nockma subexpressions, such as the standard library.

Nockma is a combinator interpreter defined as a set of reduction rules over nouns. A noun is an atom or a cell, where an atom is a natural number and a cell is an ordered pair of nouns.

The Nockma reduction rules as presented in the table below are applied from
top to bottom, the first rule from the top matches. Variables match any noun. As
in regular Nock4K, a formula that reduces to itself is an infinite loop, which
we define as a crash ("bottom" in formal logic). A real interpreter can
detect this crash and produce an out-of-band value instead.

The only difference between Nockma and Nock4K reduction rules is that instruction 12 is defined for scrying.

Used with the resource machine, Nockma should return a set of modifications to the state transition expressed by the input transaction:

- a set of resources to additionally create (resource plaintexts)
- a set of resources to additionally consume (addresses)
- a set of storage writes (in the format specified [here](./../rm_def/storage.md))

The Nockma standard library must include the following functions.

### Finite field

For a finite field $\mathbb{F}_n$ of order $n$, it should support:

- additive identity of type $\mathbb{F}_n$
- addition operation $\mathbb{F}_n \times \mathbb{F}_n \rightarrow \mathbb{F}_n$
- additive inversion $\mathbb{F}_n \rightarrow \mathbb{F}_n$
- multiplicative identity of type $\mathbb{F}_n$
- multiplication operation $\mathbb{F}_n \times \mathbb{F}_n \rightarrow \mathbb{F}_n$
- multiplicative inversion $\mathbb{F}_n \rightarrow \mathbb{F}_n$
- equality operation $\mathbb{F}_n \times \mathbb{F}_n \rightarrow \mathbb{F}_2$
- comparison operation based on canonical ordering $\mathbb{F}_n \times \mathbb{F}_n \rightarrow \mathbb{F}_2$

### Ring $Z_n$

For a ring $Z_n$ of unsigned integers $\mathrm{mod}~n$, it should support:

- additive identity of type $Z_n$
- addition operation $Z_n \times Z_n \rightarrow Z_n \times \mathbb{F}_2$ (with overflow indicator)
- subtraction operation $Z_n \times Z_n \rightarrow Z_n \times \mathbb{F}_2$ (with overflow indicator)
- multiplicative identity of type $Z_n$
- multiplication operation $Z_n \times Z_n \rightarrow Z_n \times \mathbb{F}_2$ (with overflow indicator)
- division operation (floor division) $Z_n \times Z_n \rightarrow Z_n$
- equality $Z_n \times Z_n \rightarrow \mathbb{F}_2$
- comparison $Z_n \times Z_n \rightarrow \mathbb{F}_2$

#### Parametrized conversion function
Additionally, it should provide a parametrized conversion function $conv_{i,j,k,l}$, where:

- $i$ is a flag that defines the input type: $i = 0$ corresponds to a finite field, $i = 1$ corresponds to a ring of unsigned integers
- $j$ is the input structure order
- $k$ is a flag that defines the output type: $k = 0$ corresponds to a finite field, $k = 1$ corresponds to a ring of unsigned integers
- $l$ is the output structure order

If the order of the input structure is bigger than the order of the output structure ($j > l$), the conversion function would return a flag (of type $\mathbb{F}_2$) indicating if overflow happened in addition to the converted value.

The conversion function must use canonical ordering and respect the inversion laws.