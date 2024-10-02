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
    ```


These types define the foundational data structures used across the identity-related engines.

```juvix
ByteString : Type := Nat;
emptyByteString : ByteString := 0;
Signable : Type := ByteString;
Commitment : Type := ByteString;
EngineReference : Type := Name;
DecryptionKey : Type := ByteString;
```

ExternalIdentity

IDParams

```juvix
type IDParams :=
  | Ed25519
  | Secp256k1
  | BLS;
```

```
syntax alias ExternalIdentity := Nat;
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
type IDBackend :=
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
```

Signature

```juvix
Signature : Type := String;
```

IdentityNameEvidence

```juvix
type IdentityNameEvidence :=
  | DotEvidence { parentSignature : Signature; child : ExternalIdentity };
```

ReadsForEvidence

```juvix
ReadsForEvidence : Type := String;
```

SignsForEvidence

```juvix
SignsForEvidence : Type := String;
```