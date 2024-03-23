# SubscribeDynamicConfigResponseV1

## Purpose

<!-- ANCHOR: purpose -->
Response to a [[SubscribeDynamicConfigRequestV1#subscribedynamicconfigrequestv1]].
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

*Records* with fields:
- `Config Key`: [[ConfigurationKeyV1#configurationkeyv1]]

  *The key of the dynamic configuration value the subscriber wants to subscribe to in the dynamic configuration KV-store.*

- `Success Operation`: [[SuccessOperationConfigKVStoreV1#successoperationconfigkvstorev1]]

  *The success of the operation, indicating that the subscription succeeded or failed.*

- `Epoch Timestamp`: [[EpochTimestampV1#epochtimestampv1]]

  *The wall clock time of the moment that the subscriber was subscribed to this dynamic configuration value.*

</div>
<!-- ANCHOR_END: type -->

## Values

