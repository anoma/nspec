# EngineX {V2 Template}

## Purpose (of EngineX)

`<one paragraph on the purpose>`

## EngineX-specific types

### TypeX1 

.  
.  
.  

### TypeXk

## [paradigmatic message sequence diagram] (optional)

We can use `mermaid` diagrams here.

```mermaid
sequenceDiagram
    participant Clock
    participant EngineX
    participant Engineϟ
    par Clock to EngineX
        Clock-)EngineX: timer `Decay` elapsed
    and Engineϟ in parallel
        Engineϟ-)EngineX: yo
    end
	Note right of EngineX: This explains the typical purpose of EngineX
```

The following is a good example of a larger diagram,
which concerns several engines
taken from the [v1 specs](https://specs.anoma.net/v1/architecture-2/ordering-v1.html#a-life-cycle-with-some-details).

```mermaid
sequenceDiagram
    participant User
    participant Worker
    participant ExecutionSupervisor
    participant ExecutorProcess
    User-)Worker: TransactionRequest
    Worker--)Worker: fix batch №
    Worker-)User: TransactionAck
    Worker--)Worker: Buffering & Shuffling
    Worker--)Worker: fix tx №
    Worker-)ExecutionSupervisor: spawnExecutor
    ExecutionSupervisor-)Worker: EPID
    Worker-)ExecutorProcess: ExecuteTransaction
    Worker-)Shard: KVSAcquireLock
    Shard-)Worker: KVSLockAcquired
    Worker-)Shard: UpdateSeenAll
    activate ExecutorProcess
    ExecutorProcess-)Shard: KVSReadRequest
    Shard-)ExecutorProcess: KVSRead
    ExecutorProcess-)Shard: KVSWrite(Request)
    %%    ExecutorProcess-)WhereToIdontKnow: pub sub information of execution data
    ExecutorProcess-)User: ExecutionSummary
    ExecutorProcess-)Worker: ExecutorFinished
    deactivate ExecutorProcess
```

For an engine page,
it may be sufficient to
"cut out" a portion of such a larger diagram, or
mark it as in the following variation of the previous diagram.


```mermaid
sequenceDiagram
    participant User
    participant Worker
    participant ExecutionSupervisor
    participant ExecutorProcess
    User-)Worker: TransactionRequest
    Worker--)Worker: fix batch №
    Worker-)User: TransactionAck
    Worker--)Worker: Buffering & Shuffling
    Worker--)Worker: fix tx №
    rect rgb(191, 223, 255)
      note right of Worker: ExecutionSupervisor in action
      Worker-)ExecutionSupervisor: spawnExecutor
      ExecutionSupervisor-)Worker: EPID
    end
    Worker-)ExecutorProcess: ExecuteTransaction
    Worker-)Shard: KVSAcquireLock
    Shard-)Worker: KVSLockAcquired
    Worker-)Shard: UpdateSeenAll
    activate ExecutorProcess
    ExecutorProcess-)Shard: KVSReadRequest
    Shard-)ExecutorProcess: KVSRead
    ExecutorProcess-)Shard: KVSWrite(Request)
    %%    ExecutorProcess-)WhereToIdontKnow: pub sub information of execution data
    ExecutorProcess-)User: ExecutionSummary
    ExecutorProcess-)Worker: ExecutorFinished
    deactivate ExecutorProcess
```

## _All_ "Conversation Partners" (Engine _types_)

### Conversation Diagram (optional)

Who is talking to whom and `EngineX` in particular about what?
For a high-level overview, 
something like a [conversation diagram](https://sparxsystems.com/enterprise_architect_user_guide/16.1/modeling_languages/bpmn_2_0_conversation.html) can be helpful.
We could simply (ab-)use mermaid entity relationship diagrams here.

Taking again the example of workers in Narwhal,
the worker is in communication with other workers,
the user and the primary. 
A partial diagram would be the following.

```mermaid
erDiagram
  Primary ||--o{ WorkerHash : receive
  WorkerHash ||--|| WorkerX : sent
  WorkerX ||--|{ NewTransaction : broadcast
  NewTransaction ||--|{ MirrorWorker : listen
  User ||--o{ TransactionRequest : send
  TransactionRequest ||--|| WorkerX : receive
```

### EngineTypeX1

.  
.  
.  


### EngineTypeXm

## Guarded Actions

### Guarded action $1$ (click for details?)

.  
.  
.  

### Guarded action $n$ (click for details?)
