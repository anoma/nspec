<div class="message">

# DeleteDynamicConfigRequest

## Purpose

<!-- ANCHOR: purpose -->
Find a dynamic configuration by its key in the dynamic configuration KV-store and delete both the key and the value.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[DeleteDynamicConfigRequestV1#deletedynamicconfigrequestv1]]

{{#include ../types/delete-dynamic-config-request-v1.md:type}}

**Triggers**

[[DeleteDynamicConfigResponseV1#deletedynamicconfigresponseV1]]

{{#include ../types/delete-dynamic-config-response-v1.md:type}}

<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Performs the requested find operation in the dynamic configurations KV-store and delete both the key and the value.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Dynamic Config Engine: DeleteDynamicConfigRequest
Dynamic Config Engine -->>- Any Local Engine: DeleteDynamicConfigResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>