---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
- ID
- Identity
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.identities;
    import Stdlib.Data.String.Base open;
    import Stdlib.Trait.Ord open using {Ordering; Ord; mkOrd};
    import Data.Set.AVL open;
    import node_architecture.types.crypto open;
    import prelude open;
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
          | some minVal :=
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

fst {A B} : Pair A B -> A
  | (mkPair a _) := a;

snd {A B} : Pair A B -> B
  | (mkPair _ b) := b;
```

## Types for network identities

Types in this section are used to represent [[Identity|identities]] within the network.

### ExternalID

A unique identifier, such as a public key, represented as a natural number.

```juvix
syntax alias ExternalID := PublicKey;
```

### InternalID

A unique identifier, such as a private key, used internally within the network,
represented as a natural number.

```juvix
syntax alias InternalID := PrivateKey;
```

### Identity

A pair combining an `ExternalID` and an `InternalID`, representing the complete
identity of an entity within the network.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Commitment

A cryptographic signature, or commitment.
Signed by an internal identity and verifiable by an external identity.

```juvix
syntax alias Commitment := Signature;
```

### NodeID

Cryptographic node identity.

```juvix
syntax alias NodeID := ExternalID;
```

### TopicID

Cryptographic topic identity.

```juvix
syntax alias TopicID := ExternalID;
```

### DomainID

Cryptographic domain identity.

```juvix
syntax alias DomainID := ExternalID;
```

### EngineName

Engine instance name.
An opaque string that is unique to the local node.

```juvix
syntax alias EngineName := String;
```

### EngineID

Engine instance identity. A pair of an optional node identity (when remote) and
an engine instance name (which may not be present, stands for anonymous engine).

!!! info

    We assume that the engine instance name is unique within the node.

```juvix
EngineID : Type := Pair (Option NodeID) (Option EngineName);
```

```juvix
unknownEngineID : EngineID := mkPair none none;
```

```juvix
isLocalEngineID (eid : EngineID) : Bool :=
  case eid of {
    | mkPair none _ := true
    | _ := false
};
```

```juvix
isRemoteEngineID (eid : EngineID) : Bool := not (isLocalEngineID eid);
```

```juvix
ByteString : Type := Nat;
emptyByteString : ByteString := 0;
Signable : Type := ByteString;
axiom emptyCommitment : Commitment;
DecryptionKey : Type := ByteString;
SigningKey : Type := ByteString;
Plaintext : Type := ByteString;
Ciphertext : Type := ByteString;

syntax alias ExternalIdentity := EngineName;
```

```juvix
nameStr (name : EngineID) : String :=
  case snd name of {
    | none := ""
    | some s := s
  };
```

```juvix
nameGen (str : String) (name : EngineName) (addr : EngineID) : EngineName :=
  (name ++str "_" ++str str ++str "_" ++str nameStr addr);
```

```juvix
axiom stringCmp : String -> String -> Ordering;

instance
StringOrd : Ord String :=
  mkOrd@{
    cmp := stringCmp;
  };
```

## Types for network identities

Types in this section are used to represent [[Identity|identities]] within the network.

These types define the foundational data structures used across the identity-related engines.

IDParams

```juvix
type IDParams :=
  | Ed25519
  | Secp256k1
  | BLS;
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
