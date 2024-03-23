<div class="message">

# SubscribeDynamicConfigResponse

## Purpose

<!-- ANCHOR: purpose -->
Response to a [[SubscribeDynamicConfigRequest#subscribedynamicconfigrequest]].
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[SubscribeDynamicConfigResponseV1#subscribedynamicconfigresponsev1]]

{{#include ../types/subscribe-dynamic-config-response-v1.md:type}}

**Triggers**



<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Subscribes to a key from the dynamic configuration KV-store, to monitor value changes.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Dynamic Config Engine: SubscribeDynamicConfigRequest
Dynamic Config Engine -->>- Any Local Engine: SubscribeDynamicConfigResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>