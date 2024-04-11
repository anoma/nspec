---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<div class="message" markdown>

# LocalRandomnessGetRand

## Purpose

<!-- --8<-- [start:purpose] -->
Generate random numbers or other random data locally on the physical machine that the Anoma node is running.
<!-- --8<-- [end:purpose] -->

## Type

<!-- --8<-- [start:type] -->
**Reception:**

[[LocalRandomnessGetRandV1#localrandomnessgetrandv1]]

--8<-- "../types/local-randomness-get-rand-v1.md:type"

**Triggers**

[[LocalRandomnessGetRandResultV1#localrandomnessgetrandresultv1]]

--8<-- "../types/local-randomness-get-rand-result-v1.md:type"

<!-- --8<-- [end:type] -->

## Behavior

<!-- --8<-- [start:behavior] -->
Generates a random number or other random data.
<!-- --8<-- [end:behavior] -->

## Message Flow

<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
Any Local Engine ->>+ Local Randomness Engine: LocalRandomnessGetRand
Local Randomness Engine -->>- Any Local Engine: LocalRandomnessGetRandResult
%% --8<-- [end:sequence]
```

<!-- --8<-- [end:messages] -->

</div>
