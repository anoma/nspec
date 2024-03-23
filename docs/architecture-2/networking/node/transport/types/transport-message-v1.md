# TransportMessageV1

## Purpose

<!-- ANCHOR: purpose -->
Describe the purpose of the type.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

*Record* with fields:

- `addr`: [[TransportAddress#transportaddress]]

  *Source or destination address*

- `tprefs`: Option\<[[TransportPrefs#transportprefs]]\>

  *Transport preferences for outgoing messages*

- `expiry`: Option\<[[Time#time]]\>

  *Expiry time for outgoing messages*

- `msg`: [[P2PMessageV1#p2pmessagev1]]

  *Encapsulated message*

</div>
<!-- ANCHOR_END: type -->
