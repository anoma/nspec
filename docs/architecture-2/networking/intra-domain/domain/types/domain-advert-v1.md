# DomainAdvert

# DomainAdvertV1

## Purpose

<!-- ANCHOR: purpose -->
Advertisement of a list of peers that are members of a domain.
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
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
<!-- ANCHOR_END: type -->
