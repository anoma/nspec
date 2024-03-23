<div class="message">

# LocalWallClockGetTimeResult

## Purpose

<!-- ANCHOR: purpose -->
Response to a [[LocalWallClockGetTime#localwallclockgettime]] request. 
<!-- ANCHOR_END: purpose -->

## Type

<!-- ANCHOR: type -->
**Reception:**

[[LocalWallClockGetTimeResultV1#localwallclockgettimeresultv1]]

{{#include ../types/local-wall-clock-get-time-result-v1.md:type}}

**Triggers**

<!-- ANCHOR_END: type -->

## Behavior

<!-- ANCHOR: behavior -->
Give the current time according to the physical machine's internal clock system.
<!-- ANCHOR_END: behavior -->


## Message Flow

<!-- ANCHOR: messages -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local Wall Clock Engine: LocalWallClockGetTime
Local Wall Clock Engine -->>- Any Local Engine: LocalWallClockGetTimeResult
%% ANCHOR_END: sequence
```

<!-- ANCHOR_END: messages -->

</div>