<div class="engine">

# Static Configuration Engine

## Purpose

<!-- ANCHOR: purpose -->
The Static Configuration Engine stores static configuration of the node that may not be change by other engines at runtime.
<!-- ANCHOR_END: purpose -->

## State


## Messages Received

### [[GetStaticConfigRequest#getstaticconfigrequest]]

{{#include static-config-engine/messages/get-static-config-request.md:purpose}}

{{#include static-config-engine/messages/get-static-config-request.md:type}}


## Notifications Sent


## Message Flow


 <!-- ANCHOR: messages -->
 ```mermaid
 sequenceDiagram
 {{#include static-config-engine/messages/get-static-config-request.md:sequence}}
 ```
 <!-- ANCHOR_END: messages -->

</div>

