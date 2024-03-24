# DomainAdvert

# DomainAdvertV1

## Purpose

<!-- --8<-- [start:purpose] -->
Advertisement of a list of peers that are members of a domain.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type">

- `id`: [[DomainIdentity#domainidentity]]

  *Domain ID*

- `nodes`: Vec\<NodeIdentity\>

  *List of nodes that handle external requests from non-members*

- `version`: u32

  *Version number*

- `created`: [[Time#time]]

  *Time of creation*

- `sig`: [[Signature#signature]]

  *Signature by `id`*

</div>
<!-- --8<-- [end:type] -->
