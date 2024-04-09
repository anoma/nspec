# DomainResponse


## Purpose


<!-- --8<-- [start:purpose] -->
A response returned to a [[DomainRequest#domainrequest]].
<!-- --8<-- [end:purpose] -->

## Reception


<!-- --8<-- [start:reception] -->
- Router $\to$ [[DomainResponse#domainresponse]] $\to$ DomainRouting
- DomainRouting $\to$ [[DomainResponse#domainresponse]] $\to$ DomainRouting
- DomainRouting $\to$ [[DomainResponse#domainresponse]] $\to$ Router
<!-- --8<-- [end:reception] -->

## Structure


| Field      | Type                                           | Description                                                         |
|------------|------------------------------------------------|---------------------------------------------------------------------|
| `domain`   | *[[ExternalIdentity#externalidentity]]*        | External identity of domain                                         |
| `src`      | *[[ExternalIdentity#externalidentity]]*        | External identity of sender                                         |
| `dst`      | *[[ExternalIdentity#externalidentity]]*        | External identity of recipient                                      |
| `path`     | *Vec\<[[ExternalIdentity#externalidentity]]\>* | Reverse path of the corresponding *[[DomainRequest#domainrequest]]* |
| `protocol` | *[[Protocol#protocol]]*                        | Protocol & version used in `body`                                   |
| `body`     | *Vec\<u8\>*                                    | Serialized message body.                                            |
