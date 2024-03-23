# DomainResponse

## Purpose

<!-- ANCHOR: purpose -->
A response returned to a [[DomainRequest#domainrequest]].
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Router $\to$ [[DomainResponse#domainresponse]] $\to$ DomainRouting
- DomainRouting $\to$ [[DomainResponse#domainresponse]] $\to$ DomainRouting
- DomainRouting $\to$ [[DomainResponse#domainresponse]] $\to$ Router
<!-- ANCHOR_END: reception -->

## Structure

| Field      | Type                                           | Description                                                         |
|------------|------------------------------------------------|---------------------------------------------------------------------|
| `domain`   | *[[ExternalIdentity#externalidentity]]*        | External identity of domain                                         |
| `src`      | *[[ExternalIdentity#externalidentity]]*        | External identity of sender                                         |
| `dst`      | *[[ExternalIdentity#externalidentity]]*        | External identity of recipient                                      |
| `path`     | *Vec\<[[ExternalIdentity#externalidentity]]\>* | Reverse path of the corresponding *[[DomainRequest#domainrequest]]* |
| `protocol` | *[[Protocol#protocol]]*                        | Protocol & version used in `body`                                   |
| `body`     | *Vec\<u8\>*                                    | Serialized message body.                                            |
