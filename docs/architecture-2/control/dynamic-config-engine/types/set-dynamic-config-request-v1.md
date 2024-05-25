---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# SetDynamicConfigRequestV1

## Purpose

<!-- --8<-- [start:purpose] -->
Add a dynamic configuration to the dynamic configuration KV-store by inserting its key and the corresponding value.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Records* with fields:

- `Config Key`: [[ConfigurationKeyV1#configurationkeyv1]]

  *The key that of the dynamic configuration value that is going to be added to the dynamic configuration KV-store.*
-
- `Config Value`: [[ConfigurationValueV1#configurationvaluev1]]

  *The requested dynamic configuration value.*

</div>
<!-- --8<-- [end:type] -->

## Values

