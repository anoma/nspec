# DynamicConfigChanged

## Purpose

When a dynamic configuration value changes to which subscribers are subscribed,
they get notified in accordance with the pub-sub communication pattern.
Depending on the protocol, the updated value could require an action from a subscribed engine.

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Records* with fields:
- `Config Key`: [[ConfigurationKeyV1#configurationkeyv1]]

  *The key of the dynamic configuration value the subscriber wants to subscribe to in the dynamic configuration KV-store.*

- `Config Value`: [[ConfigurationValueV1#configurationvaluev1]]

  *The updated dynamic configuration value the subscriber is subscribed to.*

- `Epoch Timestamp`: [[A/B:EpochTimestampV1#epochtimestampv1| the epoch time of the moment the value was changed.]]

  *The epoch time of the moment the value was changed.*
-
  *The wall clock time of the moment the value was changed.*

</div>
<!-- --8<-- [end:type] -->
