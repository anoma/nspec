# MeasurementChanged

## Purpose

A notification is sent when a new measurement is recorded in the measurement database. 

## Type

<!-- ANCHOR: type -->
<div class="type">

*Records* with fields:
- `Measurement Query`: [[MeasurementQueryV1#measurementqueryv1]]

  *The measurement query the subscriber is subscribed to (from the measurement database).*

- `Measurement Query Result`: [[MeasurementQueryResultV1#measurementqueryresultv1]]

  *The measurement value from the query the subscriber is subscribed to.*

- `Epoch Timestamp`: [[EpochTimestampV1#epochtimestampv1]]

  *The wall clock time of the moment the value was recorded.*

</div>
<!-- ANCHOR_END: type -->