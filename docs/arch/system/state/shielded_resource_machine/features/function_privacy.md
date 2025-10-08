# Function privacy

Shielded resource machines may provide function privacy as a feature. When enabled, it allows to replace the RL verifying key by a fixed value. This allows to hide the RL verifying key and therefore the application it is associated with. Function privacy can be enabled for each resource in the transaction individually.

The idea is to verify the RL proof recursively in another circuit with a fixed verifying key. The outer circuit calls `verify(..)` function for the RL proof and checks that it returns `True`. It takes as input RL proof, RL instance, and other fields.

Enabling function privacy requires a couple more constraints to be verified. The relevant fields, functions, and constraints are described below.

## Relevant fields

|Context|Field|Description|
|-|-|-|
|Resource object|`logicRef`|Contains the hash of the verifying key of the logic the resource is associated with.|
|Action|`verifyingKey`|Contains the key used to verify the resource logic of the corresponding resource.|
|Action|`logicVKOuterHash`|Contains the commitment to the `logicRef`|

## Relevant functions

|Function|Description|
|-|-|
|`logicRefHash`|used to compute `logicRef` from `logicVK`. It is used for compression. For the systems where `logicVK` is already a hash, `logicRefHash` can be an identity function|
|`logicVKOuterHash`|commitment scheme used to produce the corresponding instance field. In the data privacy case, it is identity function. In the function privacy case, it has to be hiding and binding|

## Relevant constraints

3. Compliance proof: `logicVKOuterHash` is correctly computed from `logicRef`.
4. Out-of-compliance checks:

	1. `logicVKOuterHash` commits to `logicVK`

	2. `verify(verifyingKey, logicInstance, proof) = True` (here `logicInstance` is assembled from the relevant `applicationData` and other action fields, such as commitments and nullifiers)

## Comparing data and function privacy

||Data Privacy|Function Privacy|
|-|-|-|
|Action `verifyingKey`|`logicVK`(variable)|`outerVK` (fixed)|
|outer hash instantiation|identity function|hiding and binding commitment scheme|
|`logicRef` check|out of circuit | in the outer circuit|
|`verify(logicVK,...)`|out of circuit| in the outer circuit
|verifier calls|`verify(logicVK, logicInstance, proof)`|`verify(outerVK, outerInstance, proof)`|
