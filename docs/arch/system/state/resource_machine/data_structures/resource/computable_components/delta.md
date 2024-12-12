---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Delta

Resource delta is used to reason about the total quantities of different kinds of resources in transactions. For a resource `r`, its delta is computed as `r.delta() = deltaHash(r.kind(), r.quantity, extraInput)`. `extraInput` contains the extra data required to derive resource delta, e.g., randomness. It may be empty if no extra data is required.

## Delta for data structures

Delta is a computable component that can also be computed for [compliance units](./../../compliance_unit.md), [actions](./../../action.md), and [transactions](./../../transaction.md).
<!--ᚦ«wikilinks preferable»-->

Note that transactions are partitioned into actions, actions are partitioned into compliance units, and compliance units are partitioned into resources. For that reason, the mechanism for computation of the deltas of these data structures is almost the same.

1. For **compliance units**, delta is computed by using signed addition over the deltas of the resources that comprise the unit: `unit.delta() = sum(r.delta() for r in unit.consumedResources) - sum(r.delta() for r in unit.createdResources)`<!--ᚦ
«What is signed addition? Do we have (a different) interface for that? Addition has subtraction»--><!--ᚦ
«So, "compliance unit = set of resources ?"  it is defined only later/ further down in the TOC»--><!--ᚦ«
syntax is sth. like set comprehension with `for` as separator »-->
2. For **actions**, delta is computed by adding the deltas of the compliance units that comprise the action:<!--ᚦ
«So, "action = set of units?"  it is defined only later/ further down in the TOC»-->`action.delta() = sum(unit.delta() for unit in action)`. To make sure the action's delta is computed correctly, validate the compliance unit delta and make sure the action's deltas are computed using compliance unit detlas values.
3. For **transactions**, delta is computed by adding the deltas of the actions that comprise the transaction:<!--ᚦ
«So, "transaction = set of units?"  it is defined only later/ further down in the TOC»--> `transaction.delta() = sum(action.delta() for unit in transaction)`. To make sure transaction's delta is computed correctly, make sure it is computed using the validated action deltas.


!!! note

    For every data structure, the delta can also be computed directly from resource deltas that comprise it, the way it is done for compliance units.
    <!--ᚦ«... because addition is associative »-->


<!--ᚦ
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global comment
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
«
    What is the order that RM specs are ideally read?
»
-->
