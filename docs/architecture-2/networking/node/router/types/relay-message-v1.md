# RelayMessageV1

## Purpose

<!-- --8<-- [start:purpose] -->
Relayed message.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Record* with fields:

- `src`: [[NodeIdentity#nodeidentity]]

  *Source Node ID*

- `dst`: [[NodeIdentity#nodeidentity]]

  *Destination Node ID*

- `tprefs`: Option\<[[TransportPrefs#transportprefs]]\>

  *Transport preferences for outgoing messages*

- `expiry`: Option\<[[Time#time]]\>

  *Expiry time for outgoing messages*

- `msg`: Vec\<u8\>

  *Encrypted and padded [[EngineMessageV1#enginemessagev1]] or [[RelayMessageV1#relaymessagev1]]*

- `sig`: [[Signature#signature]]

  *Signature over the above fields by `src`*

</div>
<!-- --8<-- [end:type] -->
