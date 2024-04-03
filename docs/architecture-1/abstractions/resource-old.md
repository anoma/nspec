# Resource Management

This section specifies the building blocks of the Resource Management System that constitutes the contents of Messages and the substrate on which higher layers (e.g. logical DAGs representing some kind of State) are built.

## Addresses
Addresses of Resources and other objects, e.g. Resource Logics/Predicates, are computed via `hash(object)`. They are also used for Content Addressed Storage. Each field of an object should be individually hashed to provide content addressing for all elements of all layers.

## Resources
Resources are the atomic units of the system.

```haskell=
data Resource = Resource {
  header :: ResourceHeader,
  body :: ResourceBody,
}

data ResourceHeader = ResourceHeader {
  resource_logic :: ContentHash,
  prefix :: ContentHash,
  suffix :: ContentHash,
  quantity :: ContentHash,
  value :: ContentHash,
}

data ResourceBody = ResourceBody {
  resource_logic :: ResourceLogic,
  prefix :: [ContentHash],
  suffix :: Nonce,
  quantity :: Natural,
  value :: ByteString,
}
```

The dynamic resource data includes a unique Suffix, providing a partially ordered history of the immutable Resources that inhabited a type can be derived this way.

### Resource Types and Fungibility
The Type of a Resource, is determined by its Resource Logic and Prefix. Resources of the same type are fungible (i.e. interchangeable) when determining balance at the scope of a Transaction.

### Resource Logic (RL)
The Logic of a Resource is defined via a Predicate and its Arguments. It specifies under which conditions `Resources` that carry it can be created and consumed.
```haskell=
data ResourceLogic = ResourceLogic {
  predicate :: ptxData -> Bool,
  arguments :: ByteString,
}
```

Predicate Arguments must contain information about the Proof System and Controllers and can contain information about Identities and anything else is supposed to influence fungibility.

The scope of a Resource Logic is a Partial Transaction and contains all Data carried by the resources which are consumed and created in it.

```haskell=
data ptxData = ptxData {
  resources :: [Resource],
}
```

Creation of new Resources happens via Ephemeral Resources inside a partial transaction. Ephemeral meaning that they count towards balance, but are not stored long term, though the proof for their validity is. TODO Taiga: Is this correct?

!!! example

    For a fungible token, new tokens may be created with a valid signature from the issuing identity and they may be spent/consumed with a valid signature from the identity which currently owns them.

!!! note 

    The Resource Logic is tied to everything influencing the fungibility of a Resource (Proof System and Static Data), we separate Predicates and Data, not for semantic reasons, but to reduce implementation complexity. The RL can optionally call external predicates which are stored in `resource_data_dynamic` or other `Resource`s.

#### Proof System and Functional Commitment Scheme
The proof system and functional commitment scheme determine the type of privacy and soundness guarantees for shielded partial transactions. They are encoded as a ByteString. TODO Taiga: Is this correct?

TODO: How do we carry proofs and commitments through the transaction lifecycle? Do we store them with the ptx's which created them?

#### Controllers
Controllers are the Identities (e.g. consensus providers) that determine the order of (p)txs including the given Resource. The first controller in the list is known as the resource originator.
By signing a message, a Controller promises to not sign another message committing to an equivocation of the signed message.
It is recommended to assume finality only after checking Controller Signatures on (p)txs.

Precedence of Controller signatures is ordered by their position in the list, i.e. a signature from the first Controller can override signatures of all downstream Controllers.
Because of this, the list positions should correspond to Trust, from most trusted in the front, to least trusted at the end.

This way we gain the following options by using signatures of upstream Controllers:
- Resolving conflicts created by defecting Controllers.
- Updating the Controller list, when the most downstream Controller is offline or defected.

> TODO: Revise and concretise this section.
> TODO: Should this be a List or a DAG?

### Prefix
The Prefix encodes information that not affect the behavior of the Resources inhabiting it, but determines a unique subtype with the same behaviors. It can for example be a set of Random Hashes or contain the Addresses of parties relevant to higher layers, e.g. Originator and Intended users of a Resource Type.

### Suffix
The Suffix must be a nonce within the scope determined by a Prefix, to uniquely identify each resource.

> TODO: What exactly should the suffix be? Should it always be a the output of a cryptographic hash function, or just a bytestring of equivalent size? Should it be only one Hash size wide, or potentially a list as well?

### Quantity
Resources carry an integer Quantity. Resources with quantity > 1 can be split into an arbitrary amount of Resources of the same Type with Quantity of at least = 1. The splitting of Resources happens via `ptx`s using Ephemeral Resources as a dummy input.

### Value
The `Value` of the `Resource` is represented by a ByteString (i.e. the current content of the "Memory Cell" at the Resource Address) to be parsed at the application level.
It can contain information about the current owner as well as additional dynamic predicates, or Identities.

#### Owner
The current owner of a Resource. The Resource Logic can require a Signature of the owner for e.g. consumption of the Resource.

#### Additional Predicates
These can be used to, e.g. express intent for Solvers.

### Linear vs. Non-Linear Resources
Non-Linear Resources are ordering invariant and can be reused. For Linear Resources, only the unconsumed Resources that inhabit a Type can be consumed.

## Predicates
A Predicate encodes constraints for how `Resources` can be used in a `partial transaction`.

The only classes of `Predicates`, relevant to the Resource Management System are `Resource Logics`s which influence fungibility of tokens, and `Dynamic Predicates`, which do not. The latter are called `Dynamic` because they can differ within a `Resource Type`.

## Partial Transaction (ptx)
A shielded `ptx` has _k_ (currently _k_ = 2) input and _k_ output resources. Shielded `ptx`s can be cascaded, if larger input and output sets are needed.

A transparent `ptx` can have arbitrary size input and output sets, but for some use-cases where proofs and nullifiers are needed it might need to be decomposed into compatible cascaded shielded `ptx`s.

A similar approach can be used to compute a set of shielded `ptx`s simultaneously, for some potential efficiency gain.

A `ptx` is the scope for `Resource Logic`s and `Dynamic Predicates`, the validity Proof of the `ptx` is computed by Taiga and stored in the `proof` field.

A partial transaction is _valid_ if and only if the predicates of all the resources consumed and created are valid.

```haskell=
data PartialTx = PartialTx {
  input_resources :: [Resource],
  output_resources :: [Resource],
  nullifiers :: Set Nullifier,
  proof :: ByteString,
  extra_data :: Map ContentHash ByteString,
}
```

Extra data can contain e.g. additional signatures and messages.

> TODO: Do we want extra_data for `ptx`s as well?
> TODO: Do we want Executable for `ptx`s? How would they look like?

```haskell=
valid_ptx :: PartialTx -> Boolean
valid_ptx (PartialTx inr outr) = all (map (\r -> logic r inr outr) (inr <> outr))
```

> TODO: Write out details about commitment and nullifier handling in the shielded case.

### Differences between Shielded and Transparent Partial Transactions
Transparent `ptx`s are shielded `ptx`s for which we preserve the plaintext input and output Resources (or pointers to it). This way, validation of Predicates can happen at any time against the plaintext Resources.

They can still be encrypted for specific recipients.

## Commitments and Nullifiers
When a shielded transaction gets executed, the commitments of the resources (equivalent to the Resource Address) created by it are recorded by the consensus provider.
A verifiable encryption scheme should be used to prove to the consensus provider correspondence between the commitment submitted and an encrypted resource with the new owner as recepient. This encrypted resource can be stored by the consensus provider to guarantee that the recepient can fetch it.

Nullifiers can always be derived from the plaintext body of a resource and need to be included in the `ptx` consuming them.

## Transactions (tx)
Transactions provide the notion of balance for a set of `ptx`s, as well as validity for all their Predicates.

A transaction is _balanced_ if and only if the input and output sets of each Resource Type are of the same size, taking quantities into account.

A transaction is _valid_ if and only if the `ptx`s it contains are valid and it is balanced.

```haskell=
data Tx = Tx {
  partial_txs :: [PartialTx],
  executable :: Executable,
}
```

```haskell=
denomination :: Resource -> ByteString
denomination r = serialize (logic r) <> static_data r

balance :: Resource -> Balance
balance r = Balance [(denomination r, quantity r)]

balance_delta :: PartialTx -> Balance
balance_delta (PartialTx inr outr) = sum (map balance inr) - sum (map balance outr)

check_transaction :: Set PartialTx -> Boolean
check_transaction ptxs = all (map valid_ptx ptxs) && sum (map balance_delta ptxs) == 0
```
> TODO: Find a clearer/more accessible represenation than haskell syntax

> TODO: Write out details about commitment and nullifier handling in the shielded case.

### Executables
Scope = TX mandatory, ptx = optional

```haskell=
data Executable = Executable {
  read_keys :: [TyphonDBKey],
  write_keys :: [TyphonDBKey],
}
```

An executable contains the machinery to infer from the `ptx`s what is supposed to be read and written to the Typhon DB.

> TODO Typhon: Concretize this

> TODO: Specify what exactly no-op's should look like
> TODO: Where do Executables come from? How does a TX get supplied with one?

## Further Considerations

### Intent
Intent can be encoded in two ways:
1. In an unbalanced `ptx`, it is expressed as a Resource Logic of an Ephemeral Resource.
2. As side information e.g. for a solver. In this case it should reside as a Predicate in `resource_data_dynamic`.

Both of these should be derived from a user facing Intent frontend, s.t. the user only needs to specify a Predicate for the `tx`s they want to perform.

The above two approaches to encode unbalanced `ptx`s, as well as side constraints, can also be used to implement other concepts beyond intent.

### Ownership
Knowledge of the nullifier key of a Resource (i.e. owning the Resource) is necessary, but not necessarily sufficient to own a resource. Ownership might further be constrained via the Predicate which can call on Predicates in `resource_dynamic_data` or external resources.

### Resource Upgrades
If we want to upgrade the proof system or other static data of a Resource Type, we instantiate a new Resource that is backwards compatible by supporting `ptx`s which take old Resources as inputs. To prevent downgrades, decisions about ordering of "strength" of proof systems should happen at a higher layer and be checked when instantiating Resources for Upgrades.

### Relationship between Notes and Resources

There is a conceptual 1:1 correspondence between a Resource and a Note.
TODO: These names/objects should be unified and we need to do a thorough examination of what is left to do to move it into practice.

## Lifecycle of a Transaction

(*Actions in italic*, States in regular font)

### Partial Candidate Transaction (optionally created using Executable from TEL)
A candidate partial transaction is created, optionally using an Executable from the TEL. It is unbalanced.

### *Solving* (optionally using Executable from TEL)
It gets balanced either by a solver node, or directly in the user wallet, optionally using an executable from the TEL.

### Candidate Transaction
Once a set of partial candidate transactions are balanced, it becomes a Candidate Transaction.
**Note**: At this point, any predicates which are not dependent on state-after-ordering can be checked and proved.
### *Ordering*
Candidate Transactions then get ordered by Typhon, or any other consensus provider determined by the controller list in a Resource.

### Ordered Candidate Transaction
Once a `tx` has been ordered, it becomes an Ordered Candidate Transaction. It is now known which Input Resources are still available.

### *Validation*
Then Taiga 1) validates the Proofs (shielded case) / aggregates input and output resources (transparent case) and 2) validates all Predicates for all `Resources` in a `tx`.

### *Optional Execution* (optionally using Executable from the TEL)
Optional Step: The Executables from the TEL for the Execution Engine are run. E.g. executables that depend on all relevant Resources being known.

### (Validated Ordered Candidate) Transaction
Once Validation and Optional Execution are done, the last remaining step is to:

### *Apply Transaction*
The Transaction gets applied by Typhon: Commitments and Nullifiers are added to their respective trees.

### Executed/Applied Transaction
The Transaction has been applied.
