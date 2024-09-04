---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Definitions

Applications are characterised by a set of resource logics and a set of transaction functions.

$Application = (ApplicationLogic, ApplicationInterface)$, where

- $ApplicationLogic \subseteq \mathbb{F}_l$ is a set of resource logics.
- $ApplicationInterface = \{t: TransactionFunction\}$ is a set of transaction functions.

As any abstract action can be represented as a transaction consuming and creating resources of certain kinds (or a transaction function that evaluates to such a transaction), the transaction functions associated with the application represent the set of actions that the application can provide to its users. Each transaction function would require a subset of the application resource logics to approve the transaction in order to realise the desired action. The transaction function evaluated with the exact resources to be created and consumed forms a transaction.

The resources that are bound with the application resource logics are said to belong to the application and constitute the application state. When the application does not have any resources that were created but not consumed yet, the application only exists virtually but not tangibly.

The abstraction of an application is virtual - applications are not deployed or tracked in any sort of global registry, and the ARM is unaware of the existence of applications.

We define $AppKinds \subseteq \mathbb{F}_{kind}$ as a union of all resource kinds that are involved in the transaction functions that comprise the application interface.

\subsection{Composition}

Applications are composable. The composition of two (or more applications would be a composition of the corresponding logics and interfaces.

$App_12 = App_1 \circ App_2$:

- $AppLogic_{12} = AppLogic_1 \cup AppLogic_2$
- $AppInterface_{12} = AppInterface_1 \cup AppInterface_2$
- $AppKinds_{12} = AppKinds_1 \cup AppKinds_2$