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

## Architecture Motivation

Below we expound on the motivation of the interoperability mechanism. Particularly relating to the definitions of terms "forwarder contract" and "calldata resource".

### Forwarder Contracts

The core idea we start with is: the RM and specifically some applications want to be able to communicate with other contracts on Ethereum. For example, there is an ERC-20 contract, it may have some functions such as `transfer` that we are interested in calling. Another example would be a `counter` contract that stores a natural number which can be incremented. Generally, as applications on Anoma are permissionless, so is their choice regarding which contract functionality they would be interested in.

We could - theoretically - call these contracts directly, but what we are interested in is allowing calls to be made bound to certain logic enforceable through the RM. That is, we want a call to a contract `C` to be connected with some resource `R` such that only if its resource logic is satisfied, the call can induce a state change (supposing the call is successful).

As an example, we may want to create a resource connected to the increment contract described above such that the resource can only be created if its quantity matches the current value of the counter stored. Or we may want to issue a resource `R` of quantity `R.q` only if somebody has locked some tokens of the same quantity to be used inside the RM.

That means, that what we want is not just to make a call, but to make a call subject to a certain logic.

Therefore we need not only the original contract, but a place to store the logic connected to the application. For that, we need to have a forwarder contract. It will be a contract that can perform the needed calls with arbitrary constraints and store the needed resource logics making sure only specific applications will be able to perform possible operations through them.

A forwarder contract is a contract which has one required function interface: `forwardCall` accepting a logic reference and input bytes.

`forwardCall` will be called by the PA, in order to perform arbitrary logic with inputs specified.

### Calldata Resources

Interoperability requires actors on both sides: on the RM and EVM. On the EVM we need the forwarder contracts to allow arbitrary calls to be made by application developers bound to a specific application. On the RM side, we need resources representing an application to verify that a call is being made.

For that, we need to store the information regarding a call inside the context of the resource logics being evaluated. In particular, we have the `externalPayload` field inside `appData`. There we put information such as the address of the forwarder contract we call, inputs to the call, as well as the expected outputs.

As `appData` gets exposed to the resource logics they can make sure that a call is present (or absent) and will be made by the PA, returning the desired output.

At the same time, forwarder also can control which resources are able to call them. The PA other than feeding the specified inputs to the `forwardCall`, also send the logic reference of a resource calling it. This allows the forwarder contract to revert in case it does not trust the logic (and hence the inputs) of a resource making the call.

### Emergency Calls

The final piece of the puzzle to motivate are emergency calls.

While `forwardCall` is the only function that constitute the interface of a forwarder - as these are the minimal interface to interact with the PA - there are some additional functions we recommend developers to implement in order to be certain that their applications can be migratable.

In partciular, note that a Resource Machine needs a proving system. One specific component it needs is a verifier. The PA implementation uses a Risc0-supplied verifier contract. In case Risc0 find a vulnerability for the appropriate version, the verifier gets shut down. As no state change can happen without verifying the compliance and logic proofs, there will be no state changes after the shut down.

As many applications will require `forwarderCall` to be made only by the PA for good design, that would completely block the removal of any funds locked inside such forwarder contracts.

In order to mitigate this and allow for people to move their funds after the proving system gets shut down, we recommend that developers implement the `EmergencyMigratable` interface. Specifically:

```solidity
interface IEmergencyMigratable {
    function forwardEmergencyCall(bytes memory input) external returns (bytes memory output);

    function setEmergencyCaller(address newEmergencyCaller) external;

    function emergencyCaller() external view returns (address caller);
}
```

The semantics is that the designer of a forwarder contract sets up an emergecny committee when deploying the contract. The emergency committee can call `setEmergencyCaller`, which sets up the address that can use `forwardEmergencyCall` function, which implements arbitrary logic. The `setEmergencyCaller` has two constraints:

- It can only be called by the emergency committee and
- Appropriate PA was stopped

This way `forwardEmergencyCall` will only succeed if the verifier (or the PA itself) gets shut down.
