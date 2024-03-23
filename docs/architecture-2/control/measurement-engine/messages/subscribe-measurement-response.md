<div class="message">

# SubscribeMeasurementResponse

## Purpose

<!-- ANCHOR: purpose -->
After subscribed to a measurement key in the dynamic configuration KV-store to get notified when the corresponding value changes,
return a response.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[SubscribeMeasurementResponseV1#subscribemeasurementresponsev1]]

{{#include ../types/subscribe-measurement-response-v1.md:type}}

**Triggers**


<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Replies with a status after subscribed to a query from the measurement database to monitor value changes.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Measurement Engine: SubscribeMeasurementRequest
Measurement Engine -->>- Any Local Engine: SubscribeMeasurementResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>