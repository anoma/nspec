# DataChangedTimeSeriesDB

## Purpose

<!-- --8<-- [start:purpose] -->
When the value in the time series DB changes, engines interested in this information get notified.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Records* with fields:
- `Time Series DB Query`: [[TimeSeriesDBQueryV1#timeseriesdbqueryv1]]

  *The query that expresses the desire change of the time series DB.*

- `Time Series DB Data`: [[TimeSeriesDBDataV1#timeseriesdbdatav1]]

  *The changed time series data.*

- `Epoch Timestamp`: [[EpochTimestampV1#epochtimestampv1]]

  *The wall clock time of the moment the data was changed.*

</div>
<!-- --8<-- [end:type] -->