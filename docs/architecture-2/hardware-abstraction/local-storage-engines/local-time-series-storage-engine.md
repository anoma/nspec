---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# Local Time Series Storage Engine

## Purpose

The *Local Time Series Storage Engine* provides local storage and retrieval of time series data.

## State

## Messages received

### [[GetDataTimeSeriesDBRequest#getdatatimeseriesdbrequest]]

--8<-- "local-timeseries-storage-engine/messages/get-data-time-series-DB-request.md:purpose"

--8<-- "local-timeseries-storage-engine/messages/get-data-time-series-DB-request.md:type"

### [[RecordDataTimeSeriesDBRequest#recorddatatimeseriesdbrequest]]

--8<-- "local-timeseries-storage-engine/messages/record-data-time-series-DB-request.md:purpose"

--8<-- "local-timeseries-storage-engine/messages/record-data-time-series-DB-request.md:type"

### [[DeleteDataTimeSeriesDBRequest#deletedatatimeseriesdbrequest]]

--8<-- "local-timeseries-storage-engine/messages/delete-data-time-series-DB-request.md:purpose"

--8<-- "local-timeseries-storage-engine/messages/delete-data-time-series-DB-request.md:type"

## Notifications sent

### [[DataChangedTimeSeriesDB#datachangedtimeseriesdb]]

--8<-- "local-timeseries-storage-engine/notifications/data-changed-time-series-DB.md:purpose"

--8<-- "local-timeseries-storage-engine/notifications/data-changed-time-series-DB.md:type"

## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Local Time Series Storage Engine: GetDataTimeSeriesDBRequest
Local Time Series Storage Engine -->>- Any Local Engine: GetDataTimeSeriesDBResponse
Any Local Engine ->>+ Local Time Series Storage Engine: RecordDataTimeSeriesDBRequest
Local Time Series Storage Engine -->>- Any Local Engine: RecordDataTimeSeriesDBResponse
Any Local Engine ->>+ Local Time Series Storage Engine: DeleteDataTimeSeriesDBRequest
Local Time Series Storage Engine -->>- Any Local Engine: DeleteDataTimeSeriesDBResponse
%% --8<-- [end:sequence]
```
<!-- --8<-- [end:messages] -->

</div>
