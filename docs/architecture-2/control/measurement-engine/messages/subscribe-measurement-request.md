<div class="message" markdown>


# SubscribeMeasurementRequest

## Purpose

<!-- --8<-- [start:purpose] -->
Subscribe to a measurement key in the dynamic configuration KV-store to get notified when the corresponding value changes.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[SubscribeMeasurementRequestV1#subscribemeasurementrequestv1]]

--8<-- "../types/subscribe-measurement-request-v1.md:type"

**Triggers**

[[SubscribeMeasurementResponseV1#subscribemeasurementresponsev1]]

--8<-- "../types/subscribe-measurement-response-v1.md:type"

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Subscribes to a query from the measurement database to monitor value changes.
<!-- --8<-- [end:behavior] -->


## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Measurement Engine: SubscribeMeasurementRequest
Measurement Engine -->>- Any Local Engine: SubscribeMeasurementResponse
%% --8<-- [end:sequence]
```

<!-- --8<-- [end:messages] -->

</div>
