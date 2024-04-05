# Solvers

To talk about `Solving` for `Intents`, let us introduce some terminology:

## Intents
An `Intent` describes an assertion over `Resource` consumption and creation in a `Transactions` an Agent wants to perform.

In other words, this is a way for an Agent to describe which of their owned `Resources` they want to offer for consumption (along with potential `Resources` of other owners) and which `Resources` they would like to see created in turn in a `Transaction`.

!!! quote

     Assertions dictated by the rest of the system, e.g. `Balance` must also hold, independently of `Intents`.
    
To concretize that, we formulate `Intents` as [Constraint Satisfaction Problems (CSP)](./solvers/csp.md#csp).

## Solving
The role of `Solvers` is to search for sets of `Intents` such that the `Resources` on offer by different owners/`Intent` originators fulfil all 'Intents' in the set.
