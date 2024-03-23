# Backend

## Purpose

<!-- ANCHOR: purpose -->
Specifies which backend to use in order to generate or connect an identity.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">
Enumeration; one of:
- `BACKEND_LOCAL_MEMORY`
    - keeps data in local (persistent) memory
    - specifies a symmetric encryption key to encrypt the identity with
- `BACKEND_LOCAL_CONNECTION`
    - includes e.g. browser extensions, WalletConnect, Ledger
    - specifies a subtype
- `BACKEND_REMOTE_CONNECTION`
    - specifies an external identity to route requests to
</div>
<!-- ANCHOR_END: type -->