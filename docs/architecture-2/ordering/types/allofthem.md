# Types
<!-- Some generic stuff that may be re-used, leaving this undefined for now: -->
<!--
```rust!
struct Identity {}
struct Hash {}
struct Signature {}
struct NarwhalBlock {}
struct Transaction {
    // executable code and the like
}
```
-->

#### `ChainId`

Typhon might be operating one big multi-instance, several separate base ledgers, a bunch of "binary" chimera chains, etc. Each of these is identified by a single value of type `ChainId`.

```rust
/// Id of some chain/ instance/ …
type ChainId = u64
```

#### `Height`

Heights occur in different contexts and flavours, e.g., the height of a consensus instance that is running for a specific anchor block in the mempool,
the position of a block header in the chain of block headers relative to a single validator or the learner-specific height of an anchor block in the mempool ᴅᴀɢ.

```rust
/// Height
type Height = u64
```

#### `SequenceNumber`

Each transaction in a batch of transactions (or transaction requests) has a sequence number assigned by the receiving worker. This number is relative to the current batch.

```rust
/// The sequence number of a transaction in a batch.
type SequenceNumber = u64
```

#### `BatchNumber`

Batches collected by workers have consecutive numbers. Each `BatchNumber`-`SequenceNumber` pair singles out a transaction collected at a worker.

```rust
/// The batch number of a batch relative to the history of all collected batches of the worker.
type SequenceNumber = u64
```

#### `Timestamp`
[//TobiasOnTimeStamps]: # ( We'll talk about this; each transaction has a batch number and a sequence number at a specific validator; these can be considered their logical worker-local timestamp )

<!-- 👇
```rust!
/// Representation of the transaction's position in the Mempool DAG
type Timestamp = ()
```
-->

#### `ClockTime`
[//TobiasOnClockTime]: # ( What do we need this for? )

TODO: is this different from `Timestamp`?
```rust!
type ClockTime = ()
```

#### `Identity`
see [[Identity]]

```rust!
/// Representation of (composable) identity
struct Identity {}
```

#### `Hash`

A hash has the shape of sufficiently many bytes.
```rust!
/// Hash value, e.g., https://docs.rs/keccak-hash/latest/keccak_hash/struct.H256.html
type Hash = [u8; 32]
```

#### `Signature`

[//TobiasOnSignatures]: # ( well, we probably need more detail here :-/ )
```rust!
/// Digital signature
struct Signature {}
```

#### `Learner`

One can think of a learner as a group of individual with the same trust assumptions.

```rust!
/// Description of learner instances
struct Learner {
    id : Identity,
}
```

#### `Quorums`
```rust!
/// all learner-specific quorums in the shap of a map
type Quorums = std::collections::BTreeMap<Learner,LiveQuorums>
```

#### `LiveQuorums`

This is "just" a set of quorums.

```rust!
/// Description of a set of (learner-specific) qourums
type LiveQuorums = std::collections::BTreeSet<LiveQuorum>
```

#### `LiveQuorum`

This is "just" a set of validators.

```rust!
/// Description of a quorum
type LiveQuorum = std::collections::BTreeSet<ValidatorId>
```






#### `NarwhalBlockHeader`
```rust!
/// Narwhal block header
struct NarwhalBlockHeader {}
```



#### `NarwhalBlock`
```rust!
/// Narwhal block
struct NarwhalBlock {}
```

#### `Transaction`
```rust!
/// Executable code and the like
struct Transaction {}
```

#### `TransactionExecutable`
```rust!
/// Everything this transaction needs to do post-ordering, including any interesting calculations, or proof checks. TODO
struct TransactionExecutable {}
```

#### `KVSKey`
```rust!
/// Keys in the key-value-store that is state. Currently unspecified. TODO
struct KVSKey {}
```

#### `KVSDatum`
```rust!
/// Data in the key-value-store that is state. Some kind of binary blob? TODO
struct KVSDatum {}
```

### Executor API specific types
