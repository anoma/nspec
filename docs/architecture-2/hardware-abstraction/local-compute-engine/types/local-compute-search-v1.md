---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# LocalComputeSearchV1

## Purpose

<!-- --8<-- [start:purpose] -->
Perform a search operation based on a given predicate within a specified time limit (timeout).
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
<div class="type" markdown>

*Records* with fields:
- `Predicate`: [[PredicateV1#predicatev1]]

  *Predicate describing the search operation*

- `Timeout`: [[TimeoutV1#timeoutv1]]

  *Time limit after which the search operation will be terminated (if still running)*

</div>
<!-- --8<-- [end:type] -->

## Values

