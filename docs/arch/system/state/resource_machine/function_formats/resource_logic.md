---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Logic
A resource logic is a predicate associated with a resource that checks that the provided data satisfies a set of constraints. It does not require I/O communication and is represented by or can feasibly be turned into a zk-SNARK circuit if desired to support shielded execution.

Each resource logic has a set of public and private input values. Resource logics are customizable on both implementation of the ARM (different instantiations might have different requirements for all resource logics compatible with this instantiation) and resource logic creation level (each instantiation supports arbitrary resource logics as long as they satisfy the requirements). A concrete implementation of the ARM can specify more mandatory inputs and checks (e.g., if the resources are distributed in-band, resource logics have to check that the distributed encrypted value indeed encrypts the resources created/consumed in the action), but the option of custom inputs and constraints must be supported to enable different resource logic instances existing on the application level.

The proving system used to interpret resource logics must provide the following properties:

- Verifiability. It must be possible to produce and verify a proof of type $PS.Proof$ that given a certain set of inputs, the resource logic output is true value.
- The system $PS$ used to interpret resource logics must be zero-knowledge- and function-privacy-friendly to support privacy-preserving contexts.


Resource logics take as input resources created and consumed in the action:

#### Resource Logic Public Inputs

- $nfs \subseteq nfs_{tx}$
- $cms \subseteq cms_{tx}$
- $tag: \mathbb{F}_{tag}$ —  identifies the resources being checked
- $extra \subseteq tx.extra$

#### Resource Logic Private Inputs

- input resources corresponding to the elements of $nfs$
- output resource corresponding to the elements of $cms$
- custom inputs

#### Resource Logic Constraints

- for each output resource, check that the corresponding $cm$ value is derived according to the rules specified by the resource machine instance
- for each input resource, check that the corresponding $nf$ value is derived according to the rules specified by the resource machine instantiation
- custom checks