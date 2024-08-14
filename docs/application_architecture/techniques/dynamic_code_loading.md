---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Dynamic code loading

In general, code can be stored in the standard content-addressed storage. In
order to retrieve code whose identity is known ahead of time (e.g. a standard
library), this should be sufficient. In order to retrieve code dynamically
(likely with rules on how it can be changed), a resource index lookup is
necessary. A particular denomination can be associated with a series of
resources, each representing successive versions of code and containing a
reference to the code hash, with rules as desired governing how the code
associated with this name can be changed.

Code which is looked up may be evaluated in the _transaction function_ or
verified in a _resource logic_.

#### Dynamic code evaluation in a transaction function

Simply read the code (statically, or by looking up a resource) and call `eval`
or equivalent.

This system, while simple, automatically provides many nice properties: for
example, different versions of the standard library addressed statically will
automatically be deduplicated, code-pinned, and cached.

#### Dynamic code verification in a resource logic

Here, we want a slightly different behaviour: namely, to _verify_ that the code
looked up was executed correctly. In the case of a transparent proof, this
functions similarly. In the case of a shielded proof, the code reference will
need to be a verifying key, and an extra proof will need to be provided in the
transaction. The inputs which must correspond to the inputs used in the proof
must themselves be specified. This should be provided by a `verify` syscall of
sorts.