<div class="message" markdown>


# RecordDataTimeSeriesDBRequest

## Purpose

<!-- --8<-- [start:purpose] -->
Add time series data to the DB. 
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[RecordDataTimeSeriesDBRequestV1#recorddatatimeseriesdbrequestv1]]

--8<-- "../types/record-data-time-series-DB-request-v1.md:type"

**Triggers**

[[RecordDataTimeSeriesDBResponseV1#recorddatatimeseriesdbresponsev1]]

--8<-- "../types/record-data-time-series-DB-response-v1.md:type"

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Add time series data to the time series DB.
<!-- --8<-- [end:behavior] -->


## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Local Time Series DB Engine: RecordDataTimeSeriesDBRequest
Local Time Series DB Engine -->>- Any Local Engine: RecordDataTimeSeriesDBResponse
%% --8<-- [end:sequence]
```

<!-- --8<-- [end:messages] -->

</div>