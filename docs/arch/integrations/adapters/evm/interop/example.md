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

## Examples

This section is devoted to example applications showcasing EVM interop. The core example is taken from [the appropriate forwarder page](https://github.com/anoma/evm-protocol-adapter/tree/main/contracts/src/forwarders)

### ERC20 Forwarder

The ERC20 Forwarder Contract is made in order to facilitate the ability to lock `ERC20` tokens such as USDC or wrapped ETH in it.

The `forwardCall` implementation is a direct one:

We first check that the caller is the Protocol Adapter, so that no other agent can interact with the state.

```solidity
        if (msg.sender != _PROTOCOL_ADAPTER) {
            revert UnauthorizedCaller({expected: _PROTOCOL_ADAPTER, actual: msg.sender});
        }
```

afterwards we execute the call:

```solidity
output = _ERC20_CONTRACT.functionCall(input);
```
