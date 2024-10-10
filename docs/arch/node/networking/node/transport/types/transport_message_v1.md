---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TransportMessageV1

## Purpose

<!-- --8<-- [start:purpose] -->
Describe the purpose of the type.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Record* with fields:

- `addr`: [[TransportAddress#transportaddress]]

  *Source or destination address*

- `tprefs`: Option<[[TransportPrefs#transportprefs]]>

  *Transport preferences for outgoing messages*

- `expiry`: Option<[[Time#time]]>

  *Expiry time for outgoing messages*

- `msg`: [[P2PMessageV1#p2pmessagev1]]

  *Encapsulated message*

</div>
<!-- --8<-- [end:type] -->
