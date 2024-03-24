<div class="message">

# LocalWallClockGetTimeResult

## Purpose

<!-- --8<-- [start:purpose] -->
Response to a [[LocalWallClockGetTime#localwallclockgettime]] request. 
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[LocalWallClockGetTimeResultV1#localwallclockgettimeresultv1]]

{{#include ../types/local-wall-clock-get-time-result-v1.md:type}}

**Triggers**

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Give the current time according to the physical machine's internal clock system.
<!-- --8<-- [end:behavior] -->


## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local Wall Clock Engine: LocalWallClockGetTime
Local Wall Clock Engine -->>- Any Local Engine: LocalWallClockGetTimeResult
%% ANCHOR_END: sequence
```

<!-- --8<-- [end:messages] -->

</div>