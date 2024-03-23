<div class="message">

# RecordDataTimeSeriesDBResponse

## Purpose

<!-- ANCHOR: purpose -->
Response to a [[DeleteDataTimeSeriesDBRequest#deletedatatimeseriesdbrequest]].
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[DeleteDataTimeSeriesDBResponseV1#deletedatatimeseriesdbresponsev1]]

{{#include ../types/delete-data-time-series-DB-response-v1.md:type}}

**Triggers**


<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Performs the requested data record delete operation in the time series DB.
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