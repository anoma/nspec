---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - verification
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.verification_config;

    import prelude open;
    import arch.node.engines.verification_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.system.identity.identity open hiding {ExternalIdentity};
    ```

# Verification Configuration

## Overview

The Verification engine configuration contains static information for Verification engine instances.

## The Verification Configuration

The configuration of a Verification Engine instance includes the identity's verification capabilities, the address of an associated `SignsFor` engine, and a specific backend.

### `VerificationCfg`

<!-- --8<-- [start:VerificationCfg] -->
```juvix
type VerificationCfg := mk@{
  verifier : Set SignsForEvidence -> ExternalIdentity -> Verifier ByteString Backend Signable Commitment;
  backend : Backend;
  signsForEngineAddress : EngineID;
}
```
<!-- --8<-- [end:VerificationCfg] -->

???+ code "Arguments"

    `verifier`:
    : Function to generate verifier for a set of evidence and an identity.
    It takes a set of evidence, an identity, and returns a verifier.

    `backend`:
    : The backend to use for verification.

    `signsForEngineAddress`:
    : The address of the associated SignsFor engine.

#### Instantiation

<!-- --8<-- [start:verificationCfg] -->
```juvix extract-module-statements
module verification_config_example;

  verificationCfg : EngineCfg VerificationCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "verification";
      cfg := VerificationCfg.mk@{
        verifier := \{_ _ := Verifier.mkVerifier@{
          verify := \{_ _ _ := true};
          verifierHash := HASH.mkHASH@{
            ordKey := OrdKey.mkOrdKey@{
                compare := Ord.compare
            };
            hash := \{x := "0x1234abcd"};
          };
        }};
        backend := Backend.LocalMemory;
        signsForEngineAddress := mkPair none "Blah"
      };
    }
  ;
end;
```
<!-- --8<-- [end:verificationCfg] -->
