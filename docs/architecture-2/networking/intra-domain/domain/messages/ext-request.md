# ExtRequest


## Purpose


<!-- --8<-- [start:purpose] -->
External request to a domain.
<!-- --8<-- [end:purpose] -->

## Reception


<!-- --8<-- [start:reception] -->
- Any Local Engine $\to$ [[ExtRequest#extrequest]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[ExtRequest#extrequest]] $\to$ [[Domain#domain]]
<!-- --8<-- [end:reception] -->

## Structure


Defined by domain protocols.

## Effects


- When received from a local engine, the request is wrapped in a [[DomainRequest#domain-request]] and sent over the network.
- When received from the network, an [[ExtResponse#ext-response]] is sent back.

## Triggers


<!-- --8<-- [start:triggers] -->
- [[Domain#domain]] $\to$ [[DomainRequest#domain-request]] $\to$ [[Domain Routing#domain-routing]]
- [[Domain#domain]] $\to$ [[DomainResponse#domain-response]] $\to$ [[Domain Routing#domain-routing]]
<!-- --8<-- [end:triggers] -->
