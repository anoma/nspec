<div class="engine">

# Network Identity Store

## Purpose

<!-- --8<-- [start:purpose] -->
The [[Network Identity Store#network-identity-store]] (NIS) engine stores information associated with known external identities (of peers, topics, domains, and engines), such as advertised addresses and local metadata.
The information stored can come from various sources, such as local configuration, P2P protocols (e.g. peer sampling, clustering, pub/sub), other engines, or user input.

In case of peer identities, it stores known addresses along with local routing and transport preferences, latency measurements, trust metric and trust zone (e.g. local, remote).
<!-- --8<-- [end:purpose] -->

## State

### [[IdentityStore#identitystore]]

{{#include id-store/types/identity-store.md:purpose}}

{{#include id-store/types/identity-store.md:type}}

## Messages received

### [[LookupIdentityRequest#lookupidentityrequest]]

{{#include id-store/messages/lookup-identity-request.md:purpose}}

{{#include id-store/messages/lookup-identity-request.md:type}}

### [[UpdateIdentityRequest#updateidentityrequest]]

{{#include id-store/messages/update-identity-request.md:purpose}}

{{#include id-store/messages/update-identity-request.md:type}}

## Notifications sent

### [[IdentityUpdated#identityupdated]]

{{#include id-store/notifications/identity-updated.md:purpose}}

{{#include id-store/notifications/identity-updated.md:type}}

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

{{#include id-store/messages/lookup-identity-request.md:sequence}}

{{#include id-store/messages/update-identity-request.md:sequence}}
```
<!-- --8<-- [end:messages] -->

</div>
