# Capabilities

## Purpose

Specifies which capabilities to request when generating a new identity or connecting an existing one.

## Type

<!-- --8<-- [start:type] -->
<div class="type">
Enumeration; one of:
- `CAPABILITY_COMMIT`
    - The capability to generate commitments as the identity
- `CAPABILITY_DECRYPT`
    - The capability to decrypt data encrypted to the identity
- `CAPABILITY_COMMIT_AND_DECRYPT`
    - Both capabilities
</div>
<!-- --8<-- [end:type] -->