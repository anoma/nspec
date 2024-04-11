---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# RoutingScope

## Purpose

<!-- --8<-- [start:purpose] -->
Message routing scope restriction.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Enum* with values:

- `Local`

  *Routing of the message is restricted to the local node.*

- `Domain` ([[DomainIdentity#domainidentity]])

  *The message is restricted to the specified domain.*

- `Any`

  *The message may be forwarded without restrictions to remote peers.*

</div>
<!-- --8<-- [end:type] -->
