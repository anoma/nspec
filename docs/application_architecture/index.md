---
icon: material/apps
search:
  exclude: false
  boost: 2
---

# Applications

Applications consist of a set of related resource logics. The state of any
particular application is sharded across the system, and may be under many
different controllers. Applications, of course, can restrict themselves to
specific sets or paths of controllers with appropriate checks in the predicates,
but by default Anoma's architecture is designed to provide a clean separation of
application design and security choices, such that application developers can
choose the data model and predicate logic, but users can choose the security
assumptions.

It is important to note that the abstraction of an "Application" is *virtual* -
applications are not deployed or tracked in any sort of global registry -
rather, they are content-addressed by the specific logics involved. An
"Application" can be said to exist by virtue of the existence resources
referencing it, and if those resources are completely consumed it no longer
exists (except in history). In order to interact with applications, users must
know the relevant logics, which could be distributed to them through any
communications channel (including the Anoma P2P network). Applications are also
_composable_, in that state transitions for multiple applications can be
combined (atomically, if desired). Interfaces may support any combination of
applications, and no interface need to have any special permissioning.

In contrast to many blockchain systems which have separate software packages for
interfaces (wallets) and node software, Anoma is designed as a unified system,
which all nodes run - validators, gossip nodes, solvers, edge clients, etc. -
just with separate configurations to enable or disable processing, storage,
signing, etc. The Anoma node software internally handles P2P network
connections, fetching & caching state, verifying signatures (e.g. of validators,
running light clients), etc. - no interface should need to implement these, they
should just use the local API provided by the node software package.

The applications section in this specification document describes a set of
common primitives and classes of example applications suitable for different
kinds of coordination. This section is neither exhaustive nor intended to
describe particular applications in exact detail, but rather to provide an
overview and guidance for how to think about developing applications on Anoma.

- [Primitives](./primitives/index.md#primitives)

- [Kudos](./kudos.md#kudos)

- [Proof-of-stake](./system_applications/proof_of_stake.md#proof-of-stake)

- [Schelling tests](./schelling_tests.md#schelling-tests)

