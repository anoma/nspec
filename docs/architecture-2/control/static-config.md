<div class="engine" markdown>


# Static Configuration Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The Static Configuration Engine stores static configuration of the node that may not be change by other engines at runtime.
<!-- --8<-- [end:purpose] -->

## State


## Messages Received

### [[GetStaticConfigRequest#getstaticconfigrequest]]

--8<-- "static-config-engine/messages/get-static-config-request.md:purpose"

--8<-- "static-config-engine/messages/get-static-config-request.md:type"


## Notifications Sent


## Message Flow


<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram
--8<-- "static-config-engine/messages/get-static-config-request.md:sequence"
```
<!-- --8<-- [end:messages] -->

</div>
