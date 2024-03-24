<div class="message">

# LocalComputeSearch

## Purpose

<!-- --8<-- [start:purpose] -->
Perform a search operation based on a given predicate within a specified time limit (timeout).
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[LocalComputeSearchV1#localcomputesearchv1]]

{{#include ../types/local-compute-search-v1.md:type}}

**Triggers**

[[LocalComputeSearchResultV1#localcomputesearchresultv1]]

{{#include ../types/local-compute-search-result-v1.md:type}}

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Perform the requested search operation and return the computation results.
<!-- --8<-- [end:behavior] -->


## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local Compute Engine: LocalComputeSearch
Local Compute Engine -->>- Any Local Engine: LocalComputeSearchResult
%% ANCHOR_END: sequence
```

<!-- --8<-- [end:messages] -->

</div>