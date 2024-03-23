<div class="message">

# GetDynamicConfigRequest

## Purpose

<!-- ANCHOR: purpose -->
Find a dynamic configuration by its key in the dynamic configuration KV-store and return the value.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[GetDynamicConfigRequestV1#getdynamicconfigrequestv1]]

{{#include ../types/get-dynamic-config-request-v1.md:type}}

**Triggers**

[[GetDynamicConfigResponseV1#getdynamicconfigresponsev1]]

{{#include ../types/get-dynamic-config-response-v1.md:type}}

<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Performs the requested search operation in the dynamic configurations KV-store and returns the value.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Dynamic Config Engine: GetDynamicConfigRequest
Dynamic Config Engine -->>- Any Local Engine: GetDynamicConfigResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>