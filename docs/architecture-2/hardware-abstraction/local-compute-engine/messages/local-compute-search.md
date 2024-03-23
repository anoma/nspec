<div class="message">

# LocalComputeSearch

## Purpose

<!-- ANCHOR: purpose -->
Perform a search operation based on a given predicate within a specified time limit (timeout).
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[LocalComputeSearchV1#localcomputesearchv1]]

{{#include ../types/local-compute-search-v1.md:type}}

**Triggers**

[[LocalComputeSearchResultV1#localcomputesearchresultv1]]

{{#include ../types/local-compute-search-result-v1.md:type}}

<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Perform the requested search operation and return the computation results.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local Compute Engine: LocalComputeSearch
Local Compute Engine -->>- Any Local Engine: LocalComputeSearchResult
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>