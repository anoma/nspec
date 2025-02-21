---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - compliance-unit
  - resource-machine
  - type
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.compliance_unit;
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

    import arch.system.types.delta open;
    import arch.system.types.resource open;
    import arch.system.types.nullifier open;
    import arch.system.types.commitment open;
    import arch.system.types.nullifierkey open;
    import arch.system.types.proving_system open;
    import arch.system.types.compliance_proving_system open;
    ```

# Compliance Unit

A **compliance unit** partitions consumed and created resources for a single
compliance proof. It references a *compliance instance* to expand its actual
data, as well as the verifying key, the cryptographic proof, and so on. This
file defines:

- The `ComplianceUnit` type,
- A `HasDelta` instance that re-derives the unit's delta by summing resource deltas,
- Functions `consumed`, `created`, `createComplianceUnit` and `verifyComplianceUnit` (fromr the doc's interface).

## The `ComplianceUnit` Type

The doc states that a compliance unit has:

1. A reference to the **compliance proving system** used,
2. The verifying key,
3. A reference to an instance,
4. A `delta : DeltaHash`,
5. A `proof : Proof`.

```juvix
axiom ReferenceInstance : Type;
axiom dereference : ReferenceInstance -> ComplianceInstance;

type ComplianceUnit A
  (Proof : Type)
  (VerifyingKey : Type)
  (ProvingKey : Type)
:= mkComplianceUnit {
    system     : ComplianceProvingSystem A Proof VerifyingKey ProvingKey;
    vk         : VerifyingKey;
    refInst    : ReferenceInstance;
    delta      : DeltaHash;
    proof      : Proof
};
```

## HasDelta(ComplianceUnit)

The doc states we can re-derive the compliance unit's delta from the consumed
and created resource deltas: \(\sum(\text{consumed}) - \sum(\text{created})\).
We assert an additive group over `DeltaHash` and define a fold to hash a set of resources.
We define:

```juvix
syntax alias DeltaHashGroup := DeltaHash;

axiom groupZero : DeltaHashGroup;
axiom groupAdd  : DeltaHashGroup -> DeltaHashGroup -> DeltaHashGroup;
axiom groupSub  : DeltaHashGroup -> DeltaHashGroup -> DeltaHashGroup;

sumOfResourceDeltas
  (rList : List Resource)
  : DeltaHashGroup
  :=
    listFoldl
      (\{acc r := groupAdd acc (HasDelta.delta r)})
      groupZero
      rList;

instance
hasDeltaComplianceUnit {A}
  {Proof}
  {VerifyingKey}
  {ProvingKey}
  : HasDelta (ComplianceUnit A Proof VerifyingKey ProvingKey)
  := mkHasDelta@{
      delta := \{u :=
        case u of {
          | mkComplianceUnit sys vk rInst d pf :=
            let cInst := dereference rInst;
                consumedVal := sumOfResourceDeltas (map dereferenceConsumed (orderedSetToList (ComplianceInstance.consumed cInst)));
                createdVal  := sumOfResourceDeltas (map dereferenceCreated (orderedSetToList (ComplianceInstance.created cInst)));
            in groupSub consumedVal createdVal
        }
      }
    };
```

## `createComplianceUnit` and `verifyComplianceUnit`

The doc states:

1. `create(PS.ProvingKey, PS.Instance, PS.Proof) -> ComplianceUnit`
2. `verify(ComplianceUnit) -> Bool`

We define them top-level:

```
createComplianceUnit
  (pk : ProvingKey)
  (cInst : ComplianceInstance)
  (pr : Proof)
  : ComplianceUnit Proof VerifyingKey ProvingKey
  :=
    -- doc says we might call system.prove(...) etc.
    -- We'll do minimal logic:
    mkComplianceUnit
      { system    = ???    -- should be present in env already
      ; vk        = ???    -- unclear where this comes from
      ; refInst   = cInst
      ; delta     = unitDelta cInst  -- doc's "unitDelta"
      ; proof     = pr
      };
```

```juvix
verifyComplianceUnit
  (A Proof VerifyingKey ProvingKey : Type)
  (u : ComplianceUnit A Proof VerifyingKey ProvingKey)
  : Bool
  :=
    case u of {
    |  mkComplianceUnit sys verK rInst delt pr :=
        -- doc: returns sys.verify(verK, cInst, pr)
        ProvingSystem.verify {{ComplianceProvingSystem.baseSystem {{sys}}}} verK (dereference rInst) pr
    };
```

!!! note
    This code is partial. In a real system, `createComplianceUnit` might produce
    the proof itself via `sys.prove(pk, cInst, someWitness)`, or store references
    differently. The doc's detail aren't really clear

## `consumed` and `created` Functions

The doc says:

- `consumed(ComplianceUnit) -> Set Nullifier`
- `created(ComplianceUnit) -> Set Commitment`

```juvix
consumed (A Proof VerifyingKey ProvingKey : Type)
  (u : ComplianceUnit A Proof VerifyingKey ProvingKey)
  : OrderedSet Nullifier
  := case u of {
      | mkComplianceUnit _ _ rInst _ _ := orderedSetMap \{(k, _) := dereferenceNullifier k} (ComplianceInstance.consumed (dereference rInst))
    };

created (A Proof VerifyingKey ProvingKey : Type) {{Ord A}}
  (u : ComplianceUnit A Proof VerifyingKey ProvingKey)
  : OrderedSet (Commitment A)
  := case u of {
      | mkComplianceUnit _ _ rInst _ _ := orderedSetMap \{(k, _) := dereferenceCommitment k} (ComplianceInstance.created (dereference rInst))
    };
```
