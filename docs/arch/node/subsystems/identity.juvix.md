---
icon: material/account-circle
search:
  exclude: false
  boost: 2
tags:
  - node-architecture
  - identity-subsystem
  - index
---

???+ code "Juvix imports"

    ```juvix
    module arch.node.subsystems.identity;
    import arch.node.engines.identity_management open;
    import arch.node.engines.decryption open;
    import arch.node.engines.encryption open;
    import arch.node.engines.commitment open;
    import arch.node.engines.verification open;
    import arch.node.engines.reads_for open;
    import arch.node.engines.signs_for open;
    import arch.node.engines.naming open;
    ```

# Identity Subsystem

---

## Purpose

The *Identity Subsystem* is responsible for managing the identity of the node.

---


