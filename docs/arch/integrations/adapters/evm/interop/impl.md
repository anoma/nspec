---
icon: material/devices
search:
  exclude: false
  boost: 2
tags:
  - evm
  - resource-machine
  - protocol-adapter
markdown_extensions:
  - def_list
---

## Implementation

Below we detail the exact code using which we perform the interoperability calls. The core logic is split between the verification that can be done without making the call (done in `verify`) and after making the call (in `execute` body)

During `verify`, while going over all the verifier inputs to the resource logics (i.e. `logicVerifierInputs`), if the PA notices that `(logicVerifierInput.appData.externalPayload.length != 0)` it will assume that the resource is trying to perform a forwarder call and hence execute `_verifyForwarderCall` logic.

We get the needed data for the verification from decoding the call from the head of the `externalPayload`

```solidity
ForwarderCalldata memory call = abi.decode(input.appData.externalPayload[0].blob, (ForwarderCalldata));
```

and the resource from the `resourcePayload` head, checking the kind correspondance:

```solidity
Resource memory resource = abi.decode(input.appData.resourcePayload[0].blob, (Resource));
```

The calldata is defined as a following struct with self-evident semantics:

```solidity
struct ForwarderCalldata {
    address untrustedForwarder;
    bytes input;
    bytes output;
}
```

Now, the only thing left to check is that `resource` corresponds to the tag of the corresponding input. To check this in the case where the resource is committed, we just compute `resource.commitment()`. In the case of the nullifier, we need to also get the nullifier key from the `resourcePayload` by running

```solidity
resource.nullifier(bytes32(input.appData.resourcePayload[1].blob))
```

If the data corresponds to tags, the verification then passes.

On the `execute` the adapter runs over the actions and all `verifierLogicInputs` inside. Inside each one, we look into the `appData.resourcePayload`.

At this point we just execute the calls and make sure that the outputs correspond to the preset ones.

```solidity
        bytes memory output = IForwarder(call.untrustedForwarder).forwardCall(call.input);

        if (keccak256(output) != keccak256(call.output)) {
            revert ForwarderCallOutputMismatch({expected: call.output, actual: output});
        }
```
