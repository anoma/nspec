<div class="message" markdown>


# GetDataTimeSeriesDBResponse


## Purpose


<!-- --8<-- [start:purpose] -->
Return the queried time series data.
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
**Reception:**

[[GetDataTimeSeriesDBResponseV1#getdatatimeseriesdbresponsev1]]

--8<-- "../types/get-data-time-series-DB-response-v1.md:type"

**Triggers**


<!-- --8<-- [end:type] -->

## Behavior


<!-- --8<-- [start:behavior] -->
Return the queried time series data.
<!-- --8<-- [end:behavior] -->


## Message Flow


<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Local Time Series DB Engine: GetDataTimeSeriesDBRequest
Local Time Series DB Engine -->>- Any Local Engine: GetDataTimeSeriesDBResponse
%% --8<-- [end:sequence]
```

<!-- --8<-- [end:messages] -->

</div>
