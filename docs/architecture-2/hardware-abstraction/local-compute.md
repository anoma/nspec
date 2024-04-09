<div class="engine" markdown>

# Local Compute Engine

## Purpose

<!-- --8<-- [start:purpose] -->

The *Local Compute Engine* performs computational search tasks locally on the physical machine the Anoma node is running.
It abstracts away the details of the underlying hardware and
provides an interface for executing complex computational search tasks effectively.

<!-- --8<-- [end:purpose] -->

## State

## Messages Received

### [[LocalComputeSearch#localcomputesearch]]

--8<-- "local-compute-engine/messages/local-compute-search.md:purpose"

--8<-- "local-compute-engine/messages/local-compute-search.md:type"

## Notifications Sent

## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram
--8<-- "local-compute-engine/messages/local-compute-search.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>
