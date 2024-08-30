---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Context

The protocol does not pick a single canonical encoding scheme (serialization format) or virtual machine, both because:

- fashions in serialization schemes and virtual machines change over time, and what scheme / VM makes most sense or is most suitable depends on specific hardware and specific applications
- the protocol does not need to, and so avoiding doing so makes the protocol simpler and easier to understand, since we can abstract the implementation details of serialization schemes and virtual machines, and one can understand how the protocol works without understanding those details (or being misled into thinking that they’re specially relevant for how the protocol works, which they aren’t)

In order to facilitate interoperability between encoding schemes and virtual machines, the protocol standardises:

- a type of data types, which allows for data to be deserialized based on a known type and for inputs and outputs to functions represented in different virtual machines to be typechecked
- a multiformat for encoding schemes
- a multiformat for virtual machines
- the functions each encoding scheme must provide, and the expected properties of those functions
- the functions each virtual machine must provide, and the expected properties of those functions

# Subpages

The protocol does not pick a single canonical encoding scheme (serialization format) or virtual machine, both because:

- fashions in serialization schemes and virtual machines change over time, and what scheme / VM makes most sense or is most suitable depends on specific hardware and specific applications
- the protocol does not need to, and so avoiding doing so makes the protocol simpler and easier to understand, since we can abstract the implementation details of serialization schemes and virtual machines, and one can understand how the protocol works without understanding those details (or being misled into thinking that they’re specially relevant for how the protocol works, which they aren’t)

In order to facilitate interoperability between encoding schemes and virtual machines, the protocol standardises:

- a type of data types, which allows for data to be deserialized based on a known type and for inputs and outputs to functions represented in different virtual machines to be typechecked
- a multiformat for encoding schemes
- a multiformat for virtual machines
- the functions each encoding scheme must provide, and the expected properties of those functions
- the functions each virtual machine must provide, and the expected properties of those functions

## Content

- [Data type](./data_type.md)
- [Virtual machine](./virtual_machine.md)
- [Encoding scheme](./encoding_scheme.md)
- [Multiencoding](./multiencoding.md)