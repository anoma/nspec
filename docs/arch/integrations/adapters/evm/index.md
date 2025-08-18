---
icon: material/devices
search:
  exclude: false
  boost: 2
tags:
  - index
  - evm
  - resource-machine
  - protocol-adapter
---

# Ethereum Virtual Machine Protocol Adapter

The Ethereum Virtual Machine (EVM) protocol adapter is a smart contract written in [Solidity](https://soliditylang.org/) that can be deployed to EVM compatible chains and roll-ups to connect them to the Anoma protocol.

The current prototype is a **settlement-only** protocol adapter, i.e., it is only capable of processing fully-evaluated transaction functions and therefore does not implement the full [[Executor Engine|executor engine]] behaviour.

The implementation can be found in the [`anoma/evm-protocol-adapter` GH repo](https://github.com/anoma/evm-protocol-adapter).

## Supported Networks

For the upcoming product version only the [Sepolia network](https://ethereum.org/en/developers/docs/networks/#sepolia) will be supported.


## Contents

- [[EVM Primitive Interfaces|Primitive Interfaces]]
- [[EVM Datatypes|Datatypes]]
- [[EVM Execution Flow|Execution Flow]]
- [[EVM Interoperability]]
