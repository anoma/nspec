<div class="engine">

# Measurement Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The *Measurement Engine* stores measurements submitted by engines associated with timestamps.
These measurements could be used by various protocols. 
For example, the Networking Machine could use latency measurements to make routing decisions. 
<!-- --8<-- [end:purpose] -->

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


 <!-- --8<-- [start:messages] -->
 ```mermaid
 sequenceDiagram
 {{#include measurement-engine/messages/record-measurement-request.md:sequence}}
 {{#include measurement-engine/messages/subscribe-measurement-request.md:sequence}}
 ```
 <!-- --8<-- [end:messages] -->

</div>

