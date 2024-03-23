# ExtRequest

## Purpose

<!-- ANCHOR: purpose -->
External request to a domain.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Any Local Engine $\to$ [[ExtRequest#extrequest]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[ExtRequest#extrequest]] $\to$ [[Domain#domain]]
<!-- ANCHOR_END: reception -->

## Structure

Defined by domain protocols.

## Effects

- When received from a local engine, the request is wrapped in a [[DomainRequest#domain-request]] and sent over the network.
- When received from the network, an [[ExtResponse#ext-response]] is sent back.

## Triggers

<!-- ANCHOR: triggers -->
- [[Domain#domain]] $\to$ [[DomainRequest#domain-request]] $\to$ [[Domain Routing#domain-routing]]
- [[Domain#domain]] $\to$ [[DomainResponse#domain-response]] $\to$ [[Domain Routing#domain-routing]]
<!-- ANCHOR_END: triggers -->
