<div class="engine" markdown>


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

--8<-- "measurement-engine/messages/record-measurement-request.md:purpose"

--8<-- "measurement-engine/messages/record-measurement-request.md:type"

### [[SubscribeMeasurementRequest#subscribemeasurementrequest]]

--8<-- "measurement-engine/messages/subscribe-measurement-request.md:purpose"

--8<-- "measurement-engine/messages/subscribe-measurement-request.md:type"


## Notifications Sent

### [[MeasurementChanged#measurementchanged]]

--8<-- "measurement-engine/notifications/measurement-changed.md:purpose"

--8<-- "measurement-engine/notifications/measurement-changed.md:type"


## Message Flow


 <!-- --8<-- [start:messages] -->
 ```mermaid
 sequenceDiagram
 --8<-- "measurement-engine/messages/record-measurement-request.md:sequence"
 --8<-- "measurement-engine/messages/subscribe-measurement-request.md:sequence"
 ```
 <!-- --8<-- [end:messages] -->

</div>

