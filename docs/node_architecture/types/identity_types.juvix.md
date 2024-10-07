---
icon: octicons/container-24
search:
  exclude: false
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.types.identity_types;

    import prelude open;
    import node_architecture.basics open;
    import Stdlib.Trait.Ord open using {Ordering; Ord; mkOrd};
    import Data.Set.AVL open;
    ```

Stuff that should be importable but don't exist, for some reason.

```juvix
-- Filters the elements of an AVLTree based on a predicate function.
terminating
AVLfilter {A} {{Ord A}} (pred : A -> Bool) (t : AVLTree A) : AVLTree A :=
  let    
    merge : AVLTree A -> AVLTree A -> AVLTree A
      | t empty := t
      | empty t := t
      | t1 t2 :=
        case lookupMin t2 of {
          | nothing := t1  -- This case should not happen since t2 is non-empty
          | just minVal :=
            let newT2 := delete minVal t2;
            in balance (mknode minVal t1 newT2)
        };
  in case t of {
      | empty := empty
      | (node x _ l r) :=
        let
          terminating
          filteredLeft := AVLfilter pred l;
          terminating
          filteredRight := AVLfilter pred r;
        in case pred x of {
             | true := balance (mknode x filteredLeft filteredRight)
             | false := merge filteredLeft filteredRight
        }
        };
```


These types define the foundational data structures used across the identity-related engines.

```juvix
ByteString : Type := Nat;
emptyByteString : ByteString := 0;
Signable : Type := ByteString;
Commitment : Type := ByteString;
emptyCommitment : Commitment := 0;
DecryptionKey : Type := ByteString;
SigningKey : Type := ByteString;
Plaintext : Type := ByteString;
Ciphertext : Type := ByteString;
```

ExternalIdentity

IDParams

```juvix
type IDParams :=
  | Ed25519
  | Secp256k1
  | BLS;
```

```juvix
type ExternalIdentity :=
  | Param { param : IDParams }
  | ThresholdComposition { identities : List ExternalIdentity };

axiom ExternalIdentityCmpDummy : ExternalIdentity -> ExternalIdentity -> Ordering;

instance
ExternalIdentityOrd : Ord ExternalIdentity := 
  mkOrd@{
    cmp := ExternalIdentityCmpDummy;
  };
```

```juvix
type Backend :=
  | BackendLocalMemory
  | BackendLocalConnection { subtype : String }
  | BackendRemoteConnection { externalIdentity : ExternalIdentity };
```


Capabilities

```juvix
type Capabilities :=
  | CapabilityCommit
  | CapabilityDecrypt
  | CapabilityCommitAndDecrypt;
```

IdentityName

```juvix
type IdentityName :=
  | LocalName { name : String }
  | DotName { parent : ExternalIdentity; child : String };

axiom IdentityNameCmpDummy : IdentityName -> IdentityName -> Ordering;

instance
IdentityNameOrd : Ord IdentityName := 
  mkOrd@{
    cmp := IdentityNameCmpDummy;
  };
```

Signature

```juvix
Signature : Type := String;
```

ReadsForEvidence

```juvix
type ReadsForEvidence := mkReadsForEvidence {
  fromIdentity : ExternalIdentity;
  toIdentity : ExternalIdentity;
  proof : ByteString;
};

axiom ReadsForCmpDummy : ReadsForEvidence -> ReadsForEvidence -> Ordering;

instance
ReadsForOrd : Ord ReadsForEvidence := 
  mkOrd@{
    cmp := ReadsForCmpDummy;
  };
```

SignsForEvidence

```juvix
type SignsForEvidence := mkSignsForEvidence {
  fromIdentity : ExternalIdentity;
  toIdentity : ExternalIdentity;
  proof : ByteString; -- Placeholder for actual proof data
};

axiom SignsForCmpDummy : SignsForEvidence -> SignsForEvidence -> Ordering;

instance
SignsForOrd : Ord SignsForEvidence := 
  mkOrd@{
    cmp := SignsForCmpDummy;
  };
```

IdentityNameEvidence

```juvix
type IdentityNameEvidence := mkIdentityNameEvidence {
  identityName : IdentityName;
  externalIdentity : ExternalIdentity;
  proof : ByteString; -- Placeholder for actual proof data
};

axiom IdentityNameEvidenceCmpDummy : IdentityNameEvidence -> IdentityNameEvidence -> Ordering;

instance
IdentityNameEvidenceOrd : Ord IdentityNameEvidence := 
  mkOrd@{
    cmp := IdentityNameEvidenceCmpDummy;
  };
```