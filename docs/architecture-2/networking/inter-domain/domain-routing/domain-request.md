# DomainRequest

## Purpose

<!-- ANCHOR: purpose -->
A request sent to a domain that is delivered to any domain member.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- [[Domain]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain Routing#domain-routing]]
- [[Domain Routing#domain-routing]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain Routing#domain-routing]]
<!-- ANCHOR_END: reception -->

## Structure

| Field      | Type                                           | Description                               |
|------------|------------------------------------------------|-------------------------------------------|
| `src`      | *[[ExternalIdentity#externalidentity]]*        | External identity of sender               |
| `domain`   | *[[ExternalIdentity#externalidentity]]*        | External identity of destination domain   |
| `path`     | *Vec\<[[ExternalIdentity#externalidentity]]\>* | Path of the request, updated at each hop. |
| `protocol` | *[[Protocol#protocol]]*                        | Protocol & version used in `body`         |
| `body`     | *Vec\<u8\>*                                    | Serialized message body.                  |

## Triggers

<!-- ANCHOR: triggers -->
- [[Domain Routing#domain-routing]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain Routing#domain-routing]]
- [[Domain Routing#domain-routing]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain]]
<!-- ANCHOR_END: triggers -->
