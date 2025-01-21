---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- verification-engine
- engine-environment
---

??? quote "Juvix imports"

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
type VerificationCfg := mkVerificationCfg {
  verifier : Set SignsForEvidence -> ExternalIdentity -> Verifier ByteString Backend Signable Commitment;
  backend : Backend;
  signsForEngineAddress : EngineID;
}
```
<!-- --8<-- [end:VerificationCfg] -->

???+ quote "Arguments"

    `verifier`:
    : Function to generate verifier for a set of evidence and an identity.

    `backend`:
    : The backend to use for verification.

    `signsForEngineAddress`:
    : The address of the associated SignsFor engine.

#### Instantiation

<!-- --8<-- [start:verificationCfg] -->
```juvix extract-module-statements
module verification_config_example;

  verificationCfg : EngineCfg VerificationCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "verification";
      cfg := mkVerificationCfg@{
        verifier := \{_ _ := mkVerifier@{
          verify := \{_ _ _ := true};
          verifierHash := mkHASH@{
            ordKey := mkOrdkey@{
                compare := Ord.cmp
            };
            hash := \{x := "0x1234abcd"};
          };
        }};
        backend := BackendLocalMemory;
        signsForEngineAddress := mkPair none "Blah"
      };
    }
  ;
end;
```
<!-- --8<-- [end:verificationCfg] -->
