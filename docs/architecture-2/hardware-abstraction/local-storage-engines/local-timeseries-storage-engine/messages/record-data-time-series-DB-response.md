<div class="message">

# RecordDataTimeSeriesDBResponse

## Purpose

<!-- ANCHOR: purpose -->
Response to a [[RecordDataTimeSeriesDBRequest#recorddatatimeseriesdbrequest]].
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[RecordDataTimeSeriesDBResponseV1#recorddatatimeseriesdbresponsev1]]

{{#include ../types/record-data-time-series-DB-response-v1.md:type}}

**Triggers**


<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Performs the requested data record operation in the time series DB. 
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local Time Series DB Engine: RecordDataTimeSeriesDBRequest
Local Time Series DB Engine -->>- Any Local Engine: RecordDataTimeSeriesDBResponse
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>