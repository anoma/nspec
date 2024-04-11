---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# DeleteDataTimeSeriesDBRequest

## Purpose

<!-- --8<-- [start:purpose] -->
Delete time series data from the DB.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[DeleteDataTimeSeriesDBRequestV1#deletedatatimeseriesdbrequestv1]]

--8<-- "../types/delete-data-time-series-DB-request-v1.md:type"

**Triggers**

[[DeleteDataTimeSeriesDBResponseV1#deletedatatimeseriesdbresponsev1]]

--8<-- "../types/delete-data-time-series-DB-response-v1.md:type"

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Delete time series data from the time series DB.
<!-- --8<-- [end:behavior] -->

## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Local Time Series DB Engine: DeleteDataTimeSeriesDBRequest
Local Time Series DB Engine -->>- Any Local Engine: DeleteDataTimeSeriesDBResponse
%% --8<-- [end:sequence]
```

<!-- --8<-- [end:messages] -->

</div>
