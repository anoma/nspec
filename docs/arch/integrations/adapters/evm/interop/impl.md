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

Below we detail the exact code using which we perform the interoperability calls.

During `execute`, while going over all the verifier inputs to the resource logics, after their verificatoon we iterate over the `externalPayload` of said resource.

For each element of the list, we try to decode the blob present as follows:

```solidity
 (address untrustedForwarder, bytes memory input, bytes memory expectedOutput) =
            abi.decode(callBlob, (address, bytes, bytes));
```

The interpretation of the variable names should be clear.


At this point we just execute the calls and make sure that the outputs correspond to the preset ones. Note that the verifier provides the logic reference of the appropriate resource as an explict extra input ot the function.

```solidity
        bytes memory actualOutput =
            IForwarder(untrustedForwarder).forwardCall({logicRef: carrierLogicRef, input: input});

        if (keccak256(actualOutput) != keccak256(expectedOutput)) {
            revert ForwarderCallOutputMismatch({expected: expectedOutput, actual: actualOutput});
        }
```
