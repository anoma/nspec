# Shielded resource machine

This section of the Anoma specification describes the design of the shielded resource machine (SRM). Shielded resource machine as a class of resource machines is designed to offer privacy properties to its users.

This specification contains both the description of the design enabling the privacy properties and the concrete primitives used to instantiate a shielded resource machine. In principle, different primitives can be used to implement the same design. When more versions of SRM exist, we might separate the two parts: general SRM considerations and concrete instantiation primitives.

### Risc0 shielded resource machine

Out first implementation of the shielded resource machine is referred to as risc0 RM. It is called that because we use [RISC Zero zkVM]() to represent the compliance and logic circuits. More on RISC Zero can be found [here]().

### General RM spec divergence

All resource machines must comply with the general resource machine specification. However, certain properties of the current abstract design might be less practical or realistic for concrete designs. Developing the abstraction and concrete instantiations that have various properties at the same time allows us to discover the flaws in the abstraction. Our long-term goal is to develop an abstraction s.t. different resource machine flavours can interoperate seamlessly. Until then, this section contains an explicit list of discrepancies with the abstract resource machine specification:

|Context|Description|
|-|-|
|Proving|Instance is not a part of the input arguments to the `prove()` function. It is the output of it|
|Balance|Only balanced transactions can have valid delta proofs, i.e. `expectedBalance = 0`.|
|Delta|We do not have explicit proving and verifying keys for delta proofs|
|Logic private inputs|Not all resources from the same action must be passed as private input to logics. Only relevant resource objects are passed. Note that the action tree contains _all_ resources in the action and the root of the tree is passed as public input.|
|Compliance proof|Compliance proving and verifying keys are hardcoded in the library and are not passed explicitly as input|
|Variable size parameters|This field is not present. This is currently irrelevant.|
|Proof aggregation|The general specification doesn't account for proof aggregation at the moment.|

### Intended privacy properties

This instantiation is designed to offer privacy properties to its users. In particular, the current design offers data privacy and is accommodated to offer function privacy. Data privacy refers to the privacy of the user identity and the transaction content. Function privacy means that involved applications cannot be determined from seeing the transaction content.

1. Nullifier and commitment unlinkability: it is impossible to link the nullifier of the consumed resource to its commitment by observing the global state alone.
2. TBD
