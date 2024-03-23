<div class="engine">

# Local Wall Clock Engine

## Purpose

<!-- ANCHOR: purpose -->

The *Local Wall Clock Engine* provides a mechanism for tracking and managing time locally on the physical machine that the Anoma node is running.
It abstracts away the details of the underlying hardware and
provides an interface for getting real-time clock functionality. 

<!-- ANCHOR_END: purpose -->

## State


## Messages Received

### [[LocalWallClockGetTime#localwallclockgettime]]

{{#include local-wall-clock-engine/messages/local-wall-clock-get-time.md:purpose}}

{{#include local-wall-clock-engine/messages/local-wall-clock-get-time.md:type}}


## Notifications Sent


## Message Flow


 <!-- ANCHOR: messages -->
 ```mermaid
 sequenceDiagram
 {{#include local-wall-clock-engine/messages/local-wall-clock-get-time.md:sequence}}
 ```
 <!-- ANCHOR_END: messages -->

</div>