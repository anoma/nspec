<div class="engine">

# Measurement Engine

## Purpose

<!-- ANCHOR: purpose -->
The *Measurement Engine* stores measurements submitted by engines associated with timestamps.
These measurements could be used by various protocols. 
For example, the Networking Machine could use latency measurements to make routing decisions. 
<!-- ANCHOR_END: purpose -->

## State


## Messages Received

### [[RecordMeasurementRequest#recordmeasurementrequest]]

{{#include measurement-engine/messages/record-measurement-request.md:purpose}}

{{#include measurement-engine/messages/record-measurement-request.md:type}}

### [[SubscribeMeasurementRequest#subscribemeasurementrequest]]

{{#include measurement-engine/messages/subscribe-measurement-request.md:purpose}}

{{#include measurement-engine/messages/subscribe-measurement-request.md:type}}


## Notifications Sent

### [[MeasurementChanged#measurementchanged]]

{{#include measurement-engine/notifications/measurement-changed.md:purpose}}

{{#include measurement-engine/notifications/measurement-changed.md:type}}


## Message Flow


 <!-- ANCHOR: messages -->
 ```mermaid
 sequenceDiagram
 {{#include measurement-engine/messages/record-measurement-request.md:sequence}}
 {{#include measurement-engine/messages/subscribe-measurement-request.md:sequence}}
 ```
 <!-- ANCHOR_END: messages -->

</div>

