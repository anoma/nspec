<div class="message" markdown>


# RecordDataTimeSeriesDBResponse


## Purpose


<!-- --8<-- [start:purpose] -->
Response to a [[RecordDataTimeSeriesDBRequest#recorddatatimeseriesdbrequest]].
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
**Reception:**

[[RecordDataTimeSeriesDBResponseV1#recorddatatimeseriesdbresponsev1]]

--8<-- "../types/record-data-time-series-DB-response-v1.md:type"

**Triggers**


<!-- --8<-- [end:type] -->

## Behavior


<!-- --8<-- [start:behavior] -->
Performs the requested data record operation in the time series DB.
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
