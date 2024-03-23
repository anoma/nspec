# RoutingTable

## Purpose

<!-- ANCHOR: purpose -->
The router maintains a routing table that associates message destination identities
with either a local engine address, a list of local engines subscribed to a pub/sub topic,
a peer identity, a relay identity, or a domain identity.

The routing table is populated by lookups from the [[Network Identity Store#network-identity-store]] (NIS) engine,
and updated when the corresponding record changes in NIS,
which the Router learns about by subscribing to [[IdentityUpdated#identityupdated]] notifications.
<!-- ANCHOR_END: purpose -->

## Type

*list\<[[RoutingTableEntry#routingtableentry]]\>*
