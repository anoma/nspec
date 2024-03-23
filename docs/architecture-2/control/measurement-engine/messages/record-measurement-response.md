<div class="message">

# RecordMeasurementResponse

## Purpose

<!-- ANCHOR: purpose -->
After added a measurement performed by an engine to the measurement database, return the result of the operation. 
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[RecordMeasurementRequestV1#recordmeasurementrequestv1]]

{{#include ../types/record-measurement-request-v1.md:type}}

**Triggers**


<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Adds a measurement performed by an engine to the measurement database.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Measurement Engine: RecordMeasurementRequest
Measurement Engine -->>- Any Local Engine: RecordMeasurementResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>