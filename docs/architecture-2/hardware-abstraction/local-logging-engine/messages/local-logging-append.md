<div class="message" markdown>


# LocalLoggingAppend

## Purpose

<!-- --8<-- [start:purpose] -->
Append new values to the logbook.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

### [[LocalLoggingAppendV1#localloggingappendV1]]

--8<-- "../types/local-logging-append-v1.md:type"

**Triggers:**

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Appends the new value to the logbook.
<!-- --8<-- [end:behavior] -->


## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% ANCHOR: sequence
Any Local Engine ->>+ Local Logging Engine: LocalLoggingAppend
%% ANCHOR_END: sequence
```
<!-- --8<-- [end:messages] -->

</div>