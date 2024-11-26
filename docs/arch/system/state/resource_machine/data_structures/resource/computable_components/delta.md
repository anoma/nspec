---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Delta
Resource delta is used to reason about the total quantities of different kinds of resources in transactions. For a resource `r`, its delta is computed as `r.delta() = DeltaHash(r.kind(), r.quantity)`.

## Delta for data structures

Delta is a computable component that can also be computed for [compliance units](./../../compliance_unit.md), [actions](./../../action.md), and [transactions](./../../transaction.md). 

Note that transactions are partitioned into actions, actions are partitioned into compliance units, and compliance units are partitioned into resources. For that reason, the mechanism for computation of the deltas of these data structures is almost the same.

1. For **compliance units**, delta is computed by using signed addition over the deltas of the resources that comprise the unit: `unit.delta() = sum(r.delta() for r in unit.consumedResources) - sum(r.delta() for r in unit.createdResources)`
2. For **actions**, delta is computed by adding the deltas of the compliance units that comprise the action:
`action.delta() = sum(unit.delta() for unit in action)`. To make sure the action's delta is computed correctly, validate the compliance unit delta and make sure the action's deltas are computed using compliance unit detlas values.
3. For **transactions**, delta is computed by adding the deltas of the actions that comprise the transaction:
`transaction.delta() = sum(action.delta() for unit in transaction)`. To make sure transaction's delta is computed correctly, make sure it is computed using the validated action deltas.


!!! note
    For every data structure, the delta can also be computed directly from resource deltas that comprise it, the way it is done for compliance units.
