---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - compliance-proving-system
  - resource-machine
  - type
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.compliance_proving_system;
    import prelude open;
    import arch.system.state.resource_machine.prelude open;

    import Stdlib.Data.Fixity open;
    import Stdlib.Data.List as List open;
    import Stdlib.Data.Pair as Pair open;
    import Stdlib.Data.Unit as Unit open;
    import Stdlib.Data.Bool open;
    import Stdlib.Data.String open;
    import Stdlib.Data.Nat open;
    import Stdlib.Data.Maybe open;

    import arch.system.types.proving_system open;
    import arch.system.types.resource open;
    import arch.system.types.nullifier open;
    import arch.system.types.nullifierkey open;
    import arch.system.types.commitment open;
    import arch.system.types.commitmenttree open;
    ```

# Compliance Proving System

A **compliance proving system** is a specialized proving system used to verify
**compliance proofs**. These proofs ensure that resources are consumed and
created in a manner consistent with the resource machine’s constraints:
Merkle path validity, logic integrity, and delta correctness.

Below we define the data types for the compliance instance and witness, as
described in the compliance proof documentation, and then provide a
`ComplianceProvingSystem` trait specializing the generic `ProvingSystem`.

## Data Definitions

### Consumed Resource Witness

The doc states that each consumed resource has five data points in the witness:
1. `resource` object
2. `nullifierKey`
3. `CTreePath`
4. `commitment`
5. opening of `logicRefHash` (stored as `ByteString` below)

```juvix
type ConsumedResourceWitness A : Type :=
  mkConsumedResourceWitness
    Resource
    NullifierKey
    CTreePath
    (Commitment A)
    ByteString;
```

### Created Resource Witness

Each created resource has two data points:
1. `resource` object
2. opening of `logicRefHash` (again `ByteString`)

```juvix
type CreatedResourceWitness : Type :=
  mkCreatedResourceWitness
    Resource
    ByteString;
```

### ComplianceWitness

The doc merges all consumed resource witness data and created resource witness
data. We store them as lists in a single data structure:

```juvix
type ComplianceWitness A : Type :=
  mkComplianceWitness
    (List (ConsumedResourceWitness A))
    (List CreatedResourceWitness);
```

### ComplianceInstance

The doc states that compliance instance data has:
1. `consumed : OrderedSet (NullifierRef, RootRef, LogicRef)`
2. `created  : OrderedSet (CommitmentRef, LogicRef)`
3. `unitDelta: DeltaHash`

```juvix
type ComplianceInstance : Type :=
  mkComplianceInstance {
    consumed : (OrderedSet (Pair NullifierRef (Pair RootRef LogicRef)));
    created : (OrderedSet (Pair CommitmentRef LogicRef));
    unitDelta : DeltaHash;
  }
```

There also has to exist some method to dereference resources.

```juvix
axiom dereferenceNullifier : LogicRef -> Nullifier;
axiom dereferenceCommitment {A} : CommitmentRef -> Commitment A;

axiom dereferenceConsumed : (Pair NullifierRef (Pair RootRef LogicRef)) -> Resource;
axiom dereferenceCreated : (Pair CommitmentRef LogicRef) -> Resource;
```

## Local Constraint Checks

The doc’s constraints for each consumed resource:

1. `resourceNullifier(r, nk) == nfRef`
2. `resourceCommitment(r) == cm`
3. `resourceLogicRefHash(r) == logicRef`
4. `merkleVerify(cm, cmPath, rootRef) == true`

Analogously for created resources:

1. `resourceCommitment(r) == ...`
2. `resourceLogicRefHash(r) == logRef`

We define checks for these constraints:

NOTE: There are a bunch of functions here that aren't currently defined.

```
checkConsumedResource
  (consWitness : ConsumedResourceWitness)
  (consRef     : (Pair NullifierRef (Pair RootRef LogicRef)))
  : Bool
  := case consWitness of {
      | mkConsumedResourceWitness r nk path cm logOp :=
        case consRef of {
        | (nfRefAndRootRef, logRf) :=
          case nfRefAndRootRef of {
          | (nfRef, rootRf) :=
            let
              passNF     : Bool := nfRef == resourceNullifier r nk;
              passCommit : Bool := resourceCommitment r == cm;
              passLog    : Bool := resourceLogicRefHash r == logRf;
              passMerkle : Bool := merkleVerify cm path rootRf;
            in
            passNF && passCommit && passLog && passMerkle
          }
        }
    };

checkCreatedResource
  (creatWitness : CreatedResourceWitness)
  (creatRef     : (Pair CommitmentRef LogicRef))
  : Bool
  := case creatWitness of {
      | mkCreatedResourceWitness r logOp :=
        case creatRef of {
          | (cmRef, logRf) :=
            let passC   : Bool := commitmentHash (resourceCommitment r) == cmRef;
                passLog : Bool := resourceLogicRefHash r == logRf;
            in passC && passLog
        }
      };
```

## Trait: `ComplianceProvingSystem`

We embed a reference to a ProvingSystem specialized
to `(ComplianceInstance, ComplianceWitness)`.

```juvix
trait
type ComplianceProvingSystem A
  (Proof : Type)
  (VerifyingKey : Type)
  (ProvingKey : Type)
:= mkComplianceProvingSystem@{
    baseSystem : ProvingSystem
      Proof
      VerifyingKey
      ProvingKey
      ComplianceInstance
      (ComplianceWitness A);
};
```
