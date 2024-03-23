# EngineMessageV1

## Purpose

<!-- ANCHOR: purpose -->
A message sent between two engine instances .
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
<div class="type">

*Record* with fields:

- `src`: [[EngineIdentity#engineidentity]]

  *Source engine identity*

- `dst`: [[DestinationIdentity#destinationidentity]]

  *Destination identity*

- `id`: u64

  *Message ID: unique per `src`-`dst` pairs*

- `reply_to`: Option\<u64\>

  *`id` of a previous message this message is in reply to*

- `expiry` Option\<[[Time#time]]\>

  *Expiry time for outgoing messages.*
  *See [[P2PMessage to Transport#p2pmessage-transport|P2PMessage]] & [[TransportMessage#transportmessage]].*

- `rprefs`: Option\<[[RoutingPrefs]]\>

  *Routing preferences*

- `tprefs`: Option\<[[TransportPrefs]]\>

  *Transport preferences*

- `protocol`: [[Protocol#protocol]]

  *Protocol & version used in `body`*

- `body`: Vec\<u8\>

  *Serialized message body*

- `sig`: Option\<[[Signature#signature]]\>

  *Signature over the above fields by `src`*

</div>
<!-- ANCHOR_END: type -->
