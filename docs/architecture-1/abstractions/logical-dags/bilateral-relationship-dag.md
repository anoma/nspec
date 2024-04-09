# Bilateral relationship DAG


The bilateral (or undirected) relationship DAG tracks bilateral (undirected) relationships between pairs of identities, where both identities must consent to the relationship, but either can disestablish it. The "friendship" relationship on social media, for example, typically has this structure. The state of the bilateral relationship DAG at any point in logical time is the set of relationships created more recently than they were destroyed (if at all) by either party, i.e. the set of outstanding relationships most recently consented to by both parties.

```haskell
data Tx
  = Create Identity Identity
  | Destroy Identity Identity

type BilateralRelationshipDAG = DAG Tx
type State = Set (Identity, Identity)

validTx :: Tx -> Bool
validTx (Create a b) = verify a (1, b) && verify b (1, a)
validTx (Destroy a b) = verify a (0, b) || verify b (0, a)

validDAG :: PhysicalDAG -> BilateralRelationshipDAG -> Bool
validDAG = all validTx . subDAGBy isTx

validState :: BilateralRelationshipDAG -> State -> Bool
validState = (==) . filter createdAfterLastDestroy
```

We can also define an entanglement measure between _a_ and _b_ as `1`, if _a_ is friends with _b_, or else the mean entanglement between all identities which _a_ is friends with and _b_, parameterised by some `k` which denotes how much entanglement falls off with following distance (`k` ranges from 0 to 1):

```haskell
entanglement :: State -> Identity -> Identity -> Real
entanglement s a b = if (friends s a b) then 1
                        else k * mean (map (flip entanglement) (allFriends s a))
```

&nbsp;

Partial ordering should be sufficient for this DAG, as no transactions can conflict, so no consensus is required.
