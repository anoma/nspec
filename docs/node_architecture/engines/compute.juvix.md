---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module node_architecture.engines.compute;
```

# Compute

- *Inputs*
    - Computational searches to perform

- *Outputs*

    - Results of computational searches

- *Preferences*

    - Who to delegate computational search to

- *Accounting*
    - Computational searches actually performed, time taken

The _compute engine_ is responsible for performing expensive computation, i.e. searching for witnesses to predicates which are (in general) in the complexity class NP. Frequently, however, more efficient search algorithms will be known for particular predicates. The compute engine is designed so that local and network-accessible compute resources may be automatically balanced between based on costs and trust assumptions.

## State

The compute engine keeps in state:

- A local cache of solutions satisfying particular predicates

- A local cache of algorithms to use to solve particular predicates

```juvix
type ComputeEngineState := mkComputeEngineState {
};
```

## Input messages

Input messages to the compute engine specify:

- A _predicate_ (by hash) which a valid solution must satisfy

- An optional _algorithm_ (by hash) to use in searching

- A maximum search cost in time and space usage (after which the compute engine will stop searching), including precision requested


!!! todo

     Figure exact units for time and space bounds.

```juvix
axiom Hash : Type;
axiom Option : Type -> Type;
axiom Integer : Type;
axiom Rational : Type;
axiom Pair : Type -> Type -> Type;

type ComputeRequest := mkComputeRequest {
    predicate : Hash;
    algorithm : Option Hash;
    max_cost_time : Pair Integer Rational;
    max_cost_space : Pair Integer Rational
};
```

## Output messages

Output messages from the compute engine specify:

- The _predicate_ (by hash)

- The _algorithm_ used, if specific (by hash)

- The _solution_ found, if one was found (by hash)

- Cost (in time and space) actually incurred, and precision of cost estimates

```juvix
type ComputeResult := mkComputeResult {
    predicate : Hash;
    algorithm : Option Hash;
    solution : Option Hash;
    actual_cost_time : Pair Integer Rational;
    actual_cost_space : Pair Integer Rational;
}
```

## Internal accounting

The compute engine internally tracks available resources (time and space) available.

!!! todo

    - Queue compute requests (perhaps priority queue) to avoid overloading available resources
    - Define some message types for querying available resources
    - Think about boundaries of networked compute abstraction layer vs local compute abstraction layer
