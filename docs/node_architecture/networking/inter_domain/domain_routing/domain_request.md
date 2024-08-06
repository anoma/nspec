---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# DomainRequest

## Purpose

<!-- --8<-- [start:purpose] -->
A request sent to a domain that is delivered to any domain member.
<!-- --8<-- [end:purpose] -->

## Reception

<!-- --8<-- [start:reception] -->
- [[Domain]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain Routing#domain_routing]]
- [[Domain Routing#domain_routing]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain Routing#domain_routing]]
<!-- --8<-- [end:reception] -->

## Structure

| Field      | Type                                           | Description                               |
|------------|------------------------------------------------|-------------------------------------------|
| `src`      | *[[ExternalIdentity#externalidentity]]*        | External identity of sender               |
| `domain`   | *[[ExternalIdentity#externalidentity]]*        | External identity of destination domain   |
| `path`     | *Vec<[[ExternalIdentity#externalidentity]]>* | Path of the request, updated at each hop. |
| `protocol` | *[[Protocol#protocol]]*                        | Protocol & version used in `body`         |
| `body`     | *Vec<u8>*                                    | Serialized message body.                  |

## Triggers

<!-- --8<-- [start:triggers] -->
- [[Domain Routing#domain_routing]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain Routing#domain_routing]]
- [[Domain Routing#domain_routing]] $\to$ [[DomainRequest#domainrequest]] $\to$ [[Domain]]
<!-- --8<-- [end:triggers] -->
