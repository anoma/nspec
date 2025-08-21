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

### Forwarders

The core idea we start with is: the RM and specifically some applications want to be able to communicate with other contracts on Ethereum. For example, there is an ERC-20 contract, it may have some functions such as `transfer` that we are interested in calling. Another example would be a `counter` contract that stores a natural number which can be incremented. Generally, as applications on Anoma are permissionless, so is their choice regarding which contract functionality they would be interested in.

We could - theoretically - call these contracts directly, but what we are interested in is allowing calls to be made bound to certain logic enforceable through the RM. That is, we want a call to a contract `C` to be connected with some resource `R` such that only if its resource logic is satisfied, the call can induce a state change (supposing the call is successful).

As an example, we may want to create a resource connected to the increment contract described above such that the resource can only be created if its quantity matches the current value of the counter stored. Or we may want to ussie a resource `R` of quantity `R.q` only if somebody has locked some tokens of the same quantity to be used inside the RM.

That means, that what we want is not just to make a call, but to make a call subject to a certain logic. Moreover, we may want to bind it not just to a logic, but to the label, as kinds play an important role in application design.

Therefore we need not only the original contract, but a place to store both logic and label connected to the application. For that, we need to have a Forwarder Contract. It will be a contract that can perform the needed calls with arbitrary constraints and store the needed resource kind making sure only specific application will be able to perform possible operations through them.

A Forwarder Contract is a contract which has two functions: `calldataCarrierResourceKind` and `forwardCall`

`forwardCall` will be called by the PA, well, in order to perform arbitrary logic with inputs specified.

`calldataResourceKind` is a `view` function that exposes to the RM the kind of the resource that can specify a call to be made to the Forwarder.

### Calldata Resources

Interoperability requires actors on both sides: on the RM and EVM. On the EVM we need the Forwarder Contracts to allow arbitrary calls to be made by application developers bound to a specific application. On the RM side, we need resources representing an application to verify that a call is being made.

For that, we need to store the information regarding a call inside the context of the resource logics being evaluated. In partciular, we have the `externalPayload` field inside `appData`. There we put information such as the address of the forwarder contract we call, inputs to the call, as well as the expected outputs.

As `appData` gets exposed to the resource logics they can make sure that a call is present (or absent) and will be made by the PA, returning the desired output.

At the same time the PA makes sure that the call is accompanied by the appropriate resource using the `calldataResourceKind` function of the contract. For that `appData` also is expetced to conatain some resource plaintext information. That way we will be able to check that the plaintext has the kind specified by the corresponding forwarder contract.

Here is approximately the logic of the PA to locate these calls and make them after running `verify` on the transaction, ensuring in particular that all RM-specified checks pass:

Go through each `appData.externalPayload` of each `tag`. Recover the plantext from `appData.resourcePayload`, and check that `hash(resourcePlaintext) = tag`. This may require the PA also knowing the nullifier key if the resource is being consumed. Finally, we check that `kind(resourcePlaintext)` is the same as the return of `calldataCarrierResourcekind()`.

Then the PA performs the calls by calling `forwardCall` on the specified address with the inputs given and check that the return data is as expected.

The `tag` to which a specific call is attached is called a Calldata Resource as it is directly related to the call baing made.

### Emergency Calls

The final piece of the puzzle to motivate are emegrency calls.

While `forwardCall` and `calldataCarrierResourceKind` are the only two functions that constitute the interface of a forwarder - as these is the minimal interface to interact with the PA - there are some additional functions we recommend developers to implement in order to be certain that their applications can be migratable.

In partciular, note that a Resource Machine needs a proving system. One specific component it needs is a verifier. The PA implementation uses a Risc0-supplied verifier contract based on 2.2.2 version. In case Risc0 find a vulnerability for the appropriate version, the verifier gets shut down. As no state change can happen without verifying the compliance and logic proofs, there will be no state changes after the shut down.

As many applications will require `forwarderCall` to be made only by the PA for good design, that would completely block the removal of any funds locked inside such forwarder contracts.

In order to mitigate this and allow for people to move their funds after the proving system gets shut down, we recommend the developers to implement the `EmergencyMigratable` interface. Specifically:

```solidity
interface IEmergencyMigratable {
    function forwardEmergencyCall(bytes memory input) external returns (bytes memory output);

    function setEmergencyCaller(address newEmergencyCaller) external;

    function emergencyCaller() external view returns (address caller);
}
```

The semantics is that the designer of Forwarder Contract sets up an emeregency committee when deploying the contract. The emergency committee can call `setEmeregncyCaller`, which sets up the address that can use `forwardEmergencyCall` function, which implements arbitrary logic. The `setEmergencyCaller` has two constraints:

- It can only be called by the emergency committee and
- Risc0 Verifier for the appropriate PA was stopped

This way `forwardEmergencyCall` will only succeed if the verified gets shut down.
