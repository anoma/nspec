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

Below we detail the exact code using which we perform the interoperability calls. The core logic is run during the `execute` evaluation.

After running `verify`, the adapter runs over the actions and all `verifierLogicInputs` inside. Inside each one, we look into the `appData.resourcePayload` and `abi.decode` the inputs, resulting in

```solidity
struct ResourceForwarderCalldataPair {
    Resource carrier;
    ForwarderCalldata call;
}
```

with

```solidity
struct ForwarderCalldata {
    address untrustedForwarder;
    bytes input;
    bytes output;
}
```

We then check that the kinds of the specified resource and forwarder contract match:

```solidity
bytes32 passedKind = carrier.kind();
bytes32 fetchedKind = IForwarder(call.untrustedForwarder).calldataCarrierResourceKind();

if (passedKind != fetchedKind) {
                    revert CalldataCarrierKindMismatch({expected: fetchedKind, actual: passedKind});
                }
```

Check that the tag corresponds to the `carrier` and execute checking that the output matches:

```solidity
        bytes memory output = IForwarder(call.untrustedForwarder).forwardCall(call.input);

        if (keccak256(output) != keccak256(call.output)) {
            revert ForwarderCallOutputMismatch({expected: call.output, actual: output});
        }
```
