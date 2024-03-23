<div class="message">

# DeleteDataTimeSeriesDBRequest

## Purpose

<!-- ANCHOR: purpose -->
Delete time series data from the DB.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[DeleteDataTimeSeriesDBRequestV1#deletedatatimeseriesdbrequestv1]]

{{#include ../types/delete-data-time-series-DB-request-v1.md:type}}

**Triggers**

[[DeleteDataTimeSeriesDBResponseV1#deletedatatimeseriesdbresponsev1]]

{{#include ../types/delete-data-time-series-DB-response-v1.md:type}}

<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Delete time series data from the time series DB.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local Time Series DB Engine: DeleteDataTimeSeriesDBRequest
Local Time Series DB Engine -->>- Any Local Engine: DeleteDataTimeSeriesDBResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>