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

The Ethereum Virtual Machine (EVM) protocol adapter is a smart contract written in [Solidity](https://soliditylang.org/) that can be deployed to any EVM-compatible chain in order to allow it to support Anoma applications.

The current prototype is a **settlement-only** protocol adapter, i.e., it is only capable of processing fully-evaluated transaction functions and therefore does not implement the full [[Executor Engine|executor engine]] behaviour.

The implementation can be found in the [`anoma/evm-protocol-adapter` GH repo](https://github.com/anoma/evm-protocol-adapter).

## Supported Networks

For the upcoming product version, the Protocol Adapter will be deployed on Ethereum Mainnet, Arbitrum, and Base.


## Contents

- [[EVM Primitive Interfaces|Primitive Interfaces]]
- [[EVM Datatypes|Datatypes]]
- [[EVM Execution Flow|Execution Flow]]
- [[EVM Interoperability]]
