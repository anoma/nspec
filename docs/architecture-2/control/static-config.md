<div class="engine">

# Static Configuration Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The Static Configuration Engine stores static configuration of the node that may not be change by other engines at runtime.
<!-- --8<-- [end:purpose] -->

## State


## Messages Received

### [[GetStaticConfigRequest#getstaticconfigrequest]]

{{#include static-config-engine/messages/get-static-config-request.md:purpose}}

{{#include static-config-engine/messages/get-static-config-request.md:type}}


## Notifications Sent


## Message Flow


 <!-- --8<-- [start:messages] -->
 ```mermaid
 sequenceDiagram
 {{#include static-config-engine/messages/get-static-config-request.md:sequence}}
 ```
 <!-- --8<-- [end:messages] -->

</div>

