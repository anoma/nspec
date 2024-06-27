---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Proving system

A proving system allows proving statements about resources, which is required to create or consume a resource. Depending on the security requirements, a proving system might be instantiated, for example, by a signature scheme, a zk-SNARK, or a trivial transparent system where the properties are proven by openly verifying the properties of published data.

### Public and private inputs
To support the intended spectrum of privacy requirements, varying from the strongest (where the relationship between the published parameters does not allow an observer to infer any kind of meaningful information about the state transition) to the weakest, where no privacy is required, we divide the proving system inputs into *public* (instance) and *private* (witness). The inputs that could potentially reveal the connection between components or other kinds of sensitive information are usually considered private, and the components that have to be and can be safely published regardless of the privacy guarantees of the system would be public inputs. 

> In the context of a transparent only system, this distinction is not meaningful because all inputs are public in such a system.

### Definition

We define a set of structures required to define a proving system $PS$ as follows:

- Proof $\pi: PS.Proof$
- Instance $x: PS.Instance$ is the public input used to produce a proof.
- Witness $w: PS.Witness$ is the private input used to produce a proof.
- Proving key $pk: PS.ProvingKey$ contains the secret data required to produce a proof for a pair $(x, w)$. 
- Verifying key $vk: PS.VerifyingKey$ contains the data required, along with the witness $x$, to verify a proof $\pi$.

#### Proof record

A **proof record** carries the components required to verify a proof. It is defined as a composite structure $PR = (\pi, x, vk): ProofRecord$, where:

- $ProofRecord = PS.VerifyingKey \times PS.Instance \times PS.Proof$
- $vk: PS.VerifyingKey$
- $x: PS.Instance$
- $\pi: PS.Proof$ is the proof of the desired statement.

#### Proving system

A **proving system** $PS$ consists of a pair of algorithms, $(Prove, Verify)$:

- $Prove(pk, x, w): PS.ProvingKey \times PS.Instance \times PS.Witness \rightarrow PS.Proof$
- $Verify(pr): PS.ProofRecord \rightarrow \mathbb{F}_b$

A proof $\pi$ for which $Verify(pr) = 1$ is considered valid.

### Proving system properties

A proving system used to produce the ARM proofs should have the following properties (as defined in \cite{thaler}):

- *Completeness*. This property states that any true statement should have a convincing proof of its validity.
- *Soundness*. This property states that no false statement should have a convincing proof.
- Proving systems used to provide privacy should additionally be *zero-knowledge*, meaning that the produced proofs reveal no information other than their own validity.

### Input availability

The party responsible for creating proofs is also responsible for providing the input to the proving system. Public inputs are required to verify the proof and must be available to any party that verifies the proof; private inputs do not have to be available and can be stored locally by the proof creator. The same rule applies to custom (not specified by the ARM) public and private inputs.

