---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.notes.applications;
```

# Applications

The ARM applications are characterised by a set of resource logics and associated read and write interfaces.

$Application = (AppLogic, AppReadInterface, AppWriteInterface)$, where

1. $AppLogic \subseteq \mathbb{F}_l$ is a set of resource logics.
2. $AppWriteInterface = \{tf: TransactionFunction\}$ is a set of functions that represents what kinds of state transitions the application offers.
3. $AppReadInterface = \{pf: ProjectionFunction\}$ is a set of functions that interprete the current state. Projection functions are defined as $ProjectionFunction: AppState \rightarrow T$, where $AppState = AppResources \times AppData$, with $AppResources$ containing all resources bound to the application’s logic and $AppData$ referring to the non-linear data the application might assume.

As any abstract state transition can be represented as a transaction consuming and creating resources of certain kinds (or a transaction function that evaluates to such a transaction), the transaction functions associated with the application represent the set of actions that the application can provide to its users. Each transaction function would require a subset of the application resource logics to approve the transaction in order to realise the desired action. The transaction function evaluated with the exact resources to be created and consumed forms a transaction.

The resources that are bound with the application resource logics are said to belong to the application and, along with some non-linear data the application might assume, constitute the application state. When the application does not have any resources that were created but not consumed yet, the application only exists virtually but not tangibly.

The abstraction of an application is virtual - applications are not deployed or tracked in any sort of global registry, and the ARM is unaware of the existence of applications.

We define $AppKinds \subseteq \mathbb{F}_{kind}$ as a union of all resource kinds that are involved in the transaction functions that comprise the application interface.

## Composition

Applications are composable. The composition of two (or more) applications would be a composition of the corresponding logics and interfaces.

$App_12 = App_1 \circ App_2$:

1. $AppLogic_{12} = AppLogic_1 \cup AppLogic_2$
2. $AppWriteInterface_{12} = AppWriteInterface_1 \cup AppWriteInterface_2$
3. $AppReadInterface_{12} = AppReadInterface_1 \cup AppReadInterface_2$
4. $AppKinds_{12} = AppKinds_1 \cup AppKinds_2$

In this type of composition the order in which the applications are composed doesn't matter.

### Application extension

Application extension is a way to generate a new application starting from an existing one by enhancing the application logic and the application interface with operations on more resource kinds. The new application is dependent on the initial one, meaning that the new application logic includes constraints involving the first application resource kinds, and the new interface requires the presence of resources of the first application kinds.


## Distributed application state synchronisation

In [the controllers report](https://doi.org/10.5281/zenodo.10498997), a controller is defined as a component that
orders transactions. The resource machine is designed to work in both
single-controller and multi-controller environments, such as Anoma. In the
context of multi-controller environments, each resource contains information
about its current controller, can only be consumed on its controller, and can be
transferred from one controller to another, meaning that a new controller
becomes responsible for the correct resource consumption. Transferring a
resource can be done by consuming a resource on the old controller and creating
a similar resource on the new controller.

Applications do not have to exist within the bounds of a single controller, and can maintain a single virtual state while the application resources being distributed among multiple controllers, which forms a distributed application state. To make sure such a distributed state correctly represents the application state, state synchronisation between multiple controllers is required.

#### Controller state synchronisation

Each controller would have their own commitment tree associated with it. Treated as subtrees of a larger Merkle tree, the controller commitment trees comprise a global commitment tree, where the leaves are the roots of the controller trees.
