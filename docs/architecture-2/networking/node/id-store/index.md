---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="engine" markdown>

# Network Identity Store

## Purpose

<!-- --8<-- [start:purpose] -->
The [[Network Identity Store#network-identity-store]] (NIS) engine stores information associated with known external identities (of peers, topics, domains, and engines), such as advertised addresses and local metadata.
The information stored can come from various sources, such as local configuration, P2P protocols (e.g. peer sampling, clustering, pub/sub), other engines, or user input.

In case of peer identities, it stores known addresses along with local routing and transport preferences, latency measurements, trust metric and trust zone (e.g. local, remote).
<!-- --8<-- [end:purpose] -->

## State

### [[IdentityStore#identitystore]]

--8<-- "id-store/types/identity-store.md:purpose"

--8<-- "id-store/types/identity-store.md:type"

## Messages received

### [[LookupIdentityRequest#lookupidentityrequest]]

--8<-- "id-store/messages/lookup-identity-request.md:purpose"

--8<-- "id-store/messages/lookup-identity-request.md:type"

### [[UpdateIdentityRequest#updateidentityrequest]]

--8<-- "id-store/messages/update-identity-request.md:purpose"

--8<-- "id-store/messages/update-identity-request.md:type"

## Notifications sent

### [[IdentityUpdated#identityupdated]]

--8<-- "id-store/notifications/identity-updated.md:purpose"

--8<-- "id-store/notifications/identity-updated.md:type"

## Message flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

--8<-- "id-store/messages/lookup-identity-request.md:sequence"

--8<-- "id-store/messages/update-identity-request.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>
