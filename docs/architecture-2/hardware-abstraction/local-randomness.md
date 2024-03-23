<div class="engine">

# Local Randomness Engine

## Purpose

<!-- ANCHOR: purpose -->

The *Local Randomness Engine* generates random numbers or data locally on the physical machine that the Anoma node is running.
Randomness is important for various computing tasks such as cryptography.

<!-- ANCHOR_END: purpose -->

## State


## Messages Received

### [[LocalRandomnessGetRand#localrandomnessgetrand]]

{{#include local-randomness-engine/messages/local-randomness-get-rand.md:purpose}}

{{#include local-randomness-engine/messages/local-randomness-get-rand.md:type}}


## Notifications Sent


## Message Flow


 <!-- ANCHOR: messages -->
 ```mermaid
 sequenceDiagram
 
 {{#include local-randomness-engine/messages/local-randomness-get-rand.md:sequence}}
 ```
 <!-- ANCHOR_END: messages -->

</div>