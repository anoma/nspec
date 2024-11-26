---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# UpdateIdentityRequest

# UpdateIdentityResponse

## Purpose

<!-- --8<-- [start:purpose] -->
Update information associated with a given external identity.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[UpdateIdentityRequestV1#updateidentityrequestv1]]

--8<-- "../types/update_identity_request_v1.md:type"

**Triggers:**

[[UpdateIdentityResponseV1#updateidentityresponsev1]]

--8<-- "../types/update_identity_response_v1.md:type"
<!-- --8<-- [end:type] -->

## Behaviour

<!-- --8<-- [start:behaviour] -->
Update the provided information in the local data store.
<!-- --8<-- [end:behaviour] -->

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Network Identity Store: UpdateIdentityRequest
Network Identity Store -->>- Any Local Engine: UpdateIdentityResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>
