<div class="message">

# VerifyRequest
# VerifyResponse

## Purpose

<!-- --8<-- [start:purpose] -->
A `VerifyRequest` instructs a verification engine to verify a commitment from a particular external identity, possibly using known signs-for relationships.

A `VerifyResponse` contains the result of verifying a commitment in response to a [[VerifyRequest]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
- [[VerifyRequest]]
- [[VerifyResponse]]
<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
- Calls the `verify` method on the provided external identity, commitment, and data, and returns the result in an [[VerifyResponse]]
- If `useSignsFor` is true, uses known signs-for relationships to determine whether the commitment is valid
- If `useSignsFor` is false, only allows a commitment from the identity specifically provided
<!-- --8<-- [end:behavior] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ VerificationEngine: VerifyRequest
VerificationEngine -->>- Any Local Engine: VerifyResponse
%% ANCHOR_END: sequence
```
<!-- --8<-- [end:messages] -->

</div>
