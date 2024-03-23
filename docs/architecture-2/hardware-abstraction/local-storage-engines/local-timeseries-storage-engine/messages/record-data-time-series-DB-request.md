<div class="message">

# RecordDataTimeSeriesDBRequest

## Purpose

<!-- ANCHOR: purpose -->
Add time series data to the DB. 
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[RecordDataTimeSeriesDBRequestV1#recorddatatimeseriesdbrequestv1]]

{{#include ../types/record-data-time-series-DB-request-v1.md:type}}

**Triggers**

[[RecordDataTimeSeriesDBResponseV1#recorddatatimeseriesdbresponsev1]]

{{#include ../types/record-data-time-series-DB-response-v1.md:type}}

<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Add time series data to the time series DB.
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