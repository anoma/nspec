---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# SubscribeMeasurementResponseV1

## Purpose

<!-- --8<-- [start:purpose] -->
Response to a [[SubscribeMeasurementRequestV1#subscribemeasurementrequestv1]]
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Records* with fields:

- `Measurement Query`: [[MeasurementQueryV1#measurementqueryv1]]

  *The measurement query the subscriber is now subscribed to.*

- `Success Operation`: [[SuccessOperationMeasurementDBV1#successoperationmeasurementdbv1]]

  *The success of the operation, indicating that the subscription attempt succeeded or failed.*

- `Epoch Timestamp`: [[EpochTimestampV1#epochtimestampv1]]

  *The wall clock time of the moment that the subscriber was subscribed to this query.*

</div>
<!-- --8<-- [end:type] -->

## Values

