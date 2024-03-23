# DataChangedTimeSeriesDB

## Purpose

<!-- ANCHOR: purpose -->
When the value in the time series DB changes, engines interested in this information get notified.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

*Records* with fields:
- `Time Series DB Query`: [[TimeSeriesDBQueryV1#timeseriesdbqueryv1]]

  *The query that expresses the desire change of the time series DB.*

- `Time Series DB Data`: [[TimeSeriesDBDataV1#timeseriesdbdatav1]]

  *The changed time series data.*

- `Epoch Timestamp`: [[EpochTimestampV1#epochtimestampv1]]

  *The wall clock time of the moment the data was changed.*

</div>
<!-- ANCHOR_END: type -->