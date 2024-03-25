<div class="engine" markdown>


# Local Randomness Engine

## Purpose

<!-- --8<-- [start:purpose] -->

The *Local Randomness Engine* generates random numbers or data locally on the physical machine that the Anoma node is running.
Randomness is important for various computing tasks such as cryptography.

<!-- --8<-- [end:purpose] -->

## State


## Messages Received

### [[LocalRandomnessGetRand#localrandomnessgetrand]]

--8<-- "local-randomness-engine/messages/local-randomness-get-rand.md:purpose"

--8<-- "local-randomness-engine/messages/local-randomness-get-rand.md:type"


## Notifications Sent


## Message Flow


 <!-- --8<-- [start:messages] -->
 ```mermaid
 sequenceDiagram
 
 --8<-- "local-randomness-engine/messages/local-randomness-get-rand.md:sequence"
 ```
 <!-- --8<-- [end:messages] -->

</div>