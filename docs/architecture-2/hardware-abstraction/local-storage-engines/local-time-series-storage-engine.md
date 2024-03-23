<div class="engine">

# Local Time Series Storage Engine

## Purpose

The *Local Time Series Storage Engine* provides local storage and retrieval of time series data.

## State

## Messages received

### [[GetDataTimeSeriesDBRequest#getdatatimeseriesdbrequest]]

{{#include local-timeseries-storage-engine/messages/get-data-time-series-DB-request.md:purpose}}

{{#include local-timeseries-storage-engine/messages/get-data-time-series-DB-request.md:type}}

### [[RecordDataTimeSeriesDBRequest#recorddatatimeseriesdbrequest]]

{{#include local-timeseries-storage-engine/messages/record-data-time-series-DB-request.md:purpose}}

{{#include local-timeseries-storage-engine/messages/record-data-time-series-DB-request.md:type}}

### [[]DeleteDataTimeSeriesDBRequest#deletedatatimeseriesdbrequest]]

{{#include local-timeseries-storage-engine/messages/delete-data-time-series-DB-request.md:purpose}}

{{#include local-timeseries-storage-engine/messages/delete-data-time-series-DB-request.md:type}}

## Notifications sent

### [[DataChangedTimeSeriesDB#datachangedtimeseriesdb]]

{{#include local-timeseries-storage-engine/notifications/data-changed-time-series-DB.md:purpose}}

{{#include local-timeseries-storage-engine/notifications/data-changed-time-series-DB.md:type}}

## Message Flow


 <!-- ANCHOR: messages -->
 ```mermaid
 sequenceDiagram
 
%% ANCHOR: sequence
Any Local Engine ->>+ Local Time Series Storage Engine: GetDataTimeSeriesDBRequest
Local Time Series Storage Engine -->>- Any Local Engine: GetDataTimeSeriesDBResponse
Any Local Engine ->>+ Local Time Series Storage Engine: RecordDataTimeSeriesDBRequest
Local Time Series Storage Engine -->>- Any Local Engine: RecordDataTimeSeriesDBResponse
Any Local Engine ->>+ Local Time Series Storage Engine: DeleteDataTimeSeriesDBRequest
Local Time Series Storage Engine -->>- Any Local Engine: DeleteDataTimeSeriesDBResponse
%% ANCHOR_END: sequence
 ```
 <!-- ANCHOR_END: messages -->

</div>