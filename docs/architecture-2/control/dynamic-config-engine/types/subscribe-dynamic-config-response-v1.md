---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# SubscribeDynamicConfigResponseV1

## Purpose

<!-- --8<-- [start:purpose] -->
Response to a [[SubscribeDynamicConfigRequestV1#subscribedynamicconfigrequestv1]].
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Records* with fields:

- `Config Key`: [[ConfigurationKeyV1#configurationkeyv1]]

  *The key of the dynamic configuration value the subscriber wants to subscribe to in the dynamic configuration KV-store.*

- `Success Operation`: [[SuccessOperationConfigKVStoreV1#successoperationconfigkvstorev1]]

  *The success of the operation, indicating that the subscription succeeded or failed.*

- `Epoch Timestamp`: [[EpochTimestampV1#epochtimestampv1]]

  *The wall clock time of the moment that the subscriber was subscribed to this dynamic configuration value.*

</div>
<!-- --8<-- [end:type] -->

## Values

