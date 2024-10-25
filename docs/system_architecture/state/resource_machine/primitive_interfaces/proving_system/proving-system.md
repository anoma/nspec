# Proving system

The resource machine differentiates between three kinds of proofs, each of which can have a distinct proving system used to produce that sort of proofs

||Execution context|Constraints defined by|Are the constraints public by default?|Description
|-|-|-|-|-|
|Resource logic proof|Action|Application|No|Action is compliant with the application constraints|
|Compliance proof|Compliance unit|Resource machine instance|Yes|Action (partitioned in compliance units) is compliant with the RM rules|
|Delta proof|Transaction|Resource machine interface|Yes|Transaction is balanced|

TODO: add some thoughts about compliance and RL proving systems