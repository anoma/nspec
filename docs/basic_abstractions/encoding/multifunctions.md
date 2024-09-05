---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Multifunctions

## Multiencoding

The _multiencode_ function takes a `DataValue` and a set of preferences, and
tries to encode it in a bytestring according to those preferences. Preferences
determine which encoding scheme(s) is/are chosen, and whether or not we attempt
to convert between virtual machine representations (requiring compilation, which
may not be supported in all cases). Multiformat codes will be included to
indicate which formats are in use (see
[here](https://research.anoma.net/t/use-of-multiformats-in-the-anoma-protocol/665/7)
for a longer description of how this works). In general, canonical commitments
to data and code are made over the output of _multiencode_. Multiencoding is
also used before storing data or sending it over the network. Any party should
be able to take any piece of stored or sent data and a type and attempt to
deserialise it with _multidecode_.

```juvix
multiencode : Preferences -> DataValue -> Bytestring
```

## Multidecoding

The _multidecode_ function takes a value in bytestring representation and tries
to decode it into an internal representation, according to the multiformat
information and the encoding schemes known by the decoding party. Attempting to
decode unknown formats will result in an error.

```juvix
multidecode : Bytestring -> DataType -> Maybe DataValue
```

## Equality

Note that, in general, equality of multiencoded representations implies equality
of data values, but equality of data values does not imply equality of
multiencoded representations (as different encoding schemes may be used).
Phrased more succinctly:

1. `multiencode a = multiencode b` → `a = b`
2. `multiencode a /= multiencode b` does not imply `a != b`

## Usage

In general, canonical commitments to data and code are made over the output of
_multiencode_. Implication (1) guarantees that (subject to the usual
cryptographic assumptions) equality of two succinct commitments (cryptographic
hash function applied to the multiencoded value) implies equality of the data
values so encoded and committed to.

Multiencoding is also used before storing data or sending it over the network.
Any party who knows the encoding scheme table should be able to take any piece
of stored or sent data and deserialise it with _multidecode_.

## Multievaluation

The _multievaluate_ function evaluates the application of a function to a value.
Whenever _multievaluate_ encounters a `FunctionV n f`, it looks up the
appropriate virtual machine as specified by the natural index $n$, decodes $f$
using $decode_n$, then calls $evaluate_n$, tracking and summing the gas used in
subsequent evaluations.

!!! note

    This implies a uniform gas scale, which we elide the details of for now, but would probably require e.g. benchmarking on the hardware in question.

```juvix
multievaluate :
  DataValue ->
  [DataValue] ->
  Natural ->
  Maybe (DataValue, Natural)
```

#### Recursive multievaluation

What if one VM is passed a data value including a `FunctionV` represented in a
different VM? The VM in question can treat this code as data - in the sense that
it can examine, introspect, modify it, etc. - but it cannot treat this code as
code, since it doesn't know how to interpret functions represented in another VM
(in general). However, we can allow one VM to call another easily enough simply
by passing a pointer to `multievaluate` itself into the evaluation context.
Then, when it encounters a function encoded for a different VM which it wishes
to evaluate, the VM can simply call `multievaluate`, tracking gas consumption as
appropriate. This technique can also be used to allow for something such as a
data query, where data queries are represented as functions understood by a
specific, specialized VM.

!!! note

    There's some ABI/FFI memory layout logic to be figured out here - `multievaluate` must be called with a function and arguments formatted as `DataValue`s - this should be specified in detail.

#### Multicompilation

What if we wish to convert functions between different VM representations? We
can define a _multicompile_ function which attempts to compile functions
represented in a data value based on a set of preferences. For example,
preferences could be to convert all functions to a particular VM, or to convert
where conversions are known in some order of preference. Compilation will fail
if unknown VM conversions are attempted.

Multicompilation depends on a known set of conversions $compile_{i,j}$ which
convert between $VM_i.t$ and $VM_j.t$ representations of functions, which must
preserve extensional equality under evaluation.

```juvix
multicompile :
  Preferences ->
  DataValue ->
  Maybe DataValue
```

##### Equality proofs

With multicompilation, we can create evidence that `a = b`, where `a` and `b`
are arbitrary data values, including functions (where `multiencode a /=
multiencode b`). This evidence would consist simply of a proof that
`multicompile prefs a = b` for some preferences `prefs`. This proof could be of
varying practical forms - the verifier could simply run `multicompile`
themselves, the verifier could trust another's run of `multicompile`, or the
verifier could check a succinct proof of computational correctness. Many details
are elided here for now.

#### Smart multievaluation

With multicompilation and equality proofs, we can also define a version of
`multievaluate` which uses available evidence + preferences intelligently at
evaluation time to use certain known-to-be-equivalent versions of functions
(e.g. compiled versions) instead of others. Then known optimized versions of
functions can be used, and even something like “JIT” compilation can happen e.g.
asychronously once certain statistical thresholds are met. Optionally, this
“smart multievaluate” can *also* use known proofs of the results of certain
evaluations (instead of repeating the evaluations), where provable VMs are
involved.