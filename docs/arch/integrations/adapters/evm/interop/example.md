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

afterwards we case on the given input. The call provided can either be `Wrap`, which indicates that the user is willing to lock up funds on the forwarder in order to freely use it on the RM side, or `Unwrap`, where an owner of the RM assets wants to withdraw them back to a specified Ethereum address.

On `Wrap`, we expect the input to decode into a struct containing a Permit2 signature of a user over an action tree root provided as witness:

```solidity
        (
            , // CallType
            address from,
            ISignatureTransfer.PermitTransferFrom memory permit,
            bytes32 witness,
            bytes memory signature
        ) = abi.decode(input, (CallType, address, ISignatureTransfer.PermitTransferFrom, bytes32, bytes));
```

The signature should allow the forwarder to lock up a specified ammount of funds.

Then the forwarder runs `permitWitnessTransferFrom` and returns empty bytes.

On `Unwrap`, we decode the input as:

```solidity
        (
            , // CallType
            address token,
            address to,
            uint128 amount
        ) = abi.decode(input, (CallType, address, address, uint128));
```

and simply call `safeTransfer`, sending a specified amount of the specified token to the provided address.

### Block Time Forwarder

A block time forwarder is a trivial forwarder accessible to anyone. Its core purpose is to inform resource of whether a certain block time has passed. That is, the contract expects a certain block time as an input, and returns a comparative result ("less than", "equal", "greater than") encoded as an enum.

The implementation is trivial:

```output
        (uint48 expectedTime) = abi.decode(input, (uint48));

        uint48 currentTime = Time.timestamp();

        TimeComparison result;
        if (expectedTime < currentTime) {
            result = TimeComparison.LT;
        } else if (expectedTime > currentTime) {
            result = TimeComparison.GT;
        } else {
            result = TimeComparison.EQ;
        }

        output = abi.encode(result);
```
