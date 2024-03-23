<div class="engine">

# Local Logging Engine

## Purpose

<!-- ANCHOR: purpose -->

The *Local Logging Engine* provides capabilities for recording, monitoring, analyzing, and managing events and activities
locally on the physical machine that the Anoma node is running.
It supports diagnostic efforts, security monitoring, performance optimization, and historical analysis to ensure the stability, security, and efficiency. 

<!-- ANCHOR_END: purpose -->

## State


## Messages Received

### [[LocalLoggingAppend#localloggingappend]]

{{#include local-logging-engine/messages/local-logging-append.md:purpose}}

{{#include local-logging-engine/messages/local-logging-append.md:type}}


## Notifications Sent


## Message Flow


 <!-- ANCHOR: messages -->
 ```mermaid
 sequenceDiagram
 {{#include local-logging-engine/messages/local-logging-append.md:sequence}}
 ```
 <!-- ANCHOR_END: messages -->

</div>

