# Numerical aggregation DAG


As a simple logical DAG, consider a numerical aggregation DAG: transactions are non-negative integers, state is computed by adding, and there are no conflicts.

```haskell
type State = Integer
type Tx = Integer
type NumericalDAG = DAG Integer

validDAG : PhysicalDAG -> NumericalDAG -> Bool
validDAG = subDAGBy isNumber

validState :: NumericalDAG -> State -> Bool
validState = (==) . foldBy (+)
```
