<div class="engine">

# Local Compute Engine

## Purpose

<!-- ANCHOR: purpose -->

The *Local Compute Engine* performs computational search tasks locally on the physical machine the Anoma node is running. 
It abstracts away the details of the underlying hardware and 
provides an interface for executing complex computational search tasks effectively.

<!-- ANCHOR_END: purpose -->

## State


## Messages Received

### [[LocalComputeSearch#localcomputesearch]]

{{#include local-compute-engine/messages/local-compute-search.md:purpose}}

{{#include local-compute-engine/messages/local-compute-search.md:type}}


## Notifications Sent


## Message Flow


 <!-- ANCHOR: messages -->
 ```mermaid
 sequenceDiagram
 {{#include local-compute-engine/messages/local-compute-search.md:sequence}}
 ```
 <!-- ANCHOR_END: messages -->

</div>