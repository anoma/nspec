---
icon: material/calculator-variant
search:
  exclude: false
tags:
  - simulator
  - example
  - nockma
  - work-in-progress
---

# Increment Simulation Example

This example demonstrates a simulation of a simple network performing an increment-and-write operation distributed across multiple engines. It involves:

-   One Mempool Worker engine to coordinate transactions.
-   Two Shard engines, managing keys "a" (97) and "b" (98) respectively.
-   Two initial transactions:
    1.  Write the value 3 to key "a".
    2.  Read the value from "a", increment it, and write the result to "b".
-   Nockma programs for each transaction, executed via the `nockmaRunnable`.

The simulation uses the `selectFirstMessage` strategy and illustrates the interaction flow between the client (initiating transactions), the Mempool Worker, Shards, and Executors.

??? code "Juvix Code"

    ```juvix
    module arch.node.integration.examples.increment;

    import prelude open;
    import arch.node.types.basics open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.engine_config open;
    import arch.node.types.engine_environment open;
    import arch.node.types.engine_behaviour open;
    import arch.node.types.engine open;
    import arch.node.types.anoma_engines open;
    import arch.node.types.anoma_message open;
    import arch.node.types.anoma_config open;
    import arch.node.types.anoma_environment open;
    import arch.node.integration.simulator open;

    -- Import specific engine implementations (configs, envs, behaviours)
    import arch.node.engines.mempool_worker_config open;
    import arch.node.engines.mempool_worker_messages open;
    import arch.node.engines.mempool_worker_environment open;
    import arch.node.engines.mempool_worker_behaviour open;
    import arch.node.engines.shard_config open;
    import arch.node.engines.shard_environment open;
    import arch.node.engines.shard_behaviour open;
    import arch.node.engines.executor_config open;
    import arch.node.engines.executor_environment open;
    import arch.node.engines.executor_behaviour open;

    -- Nockma related imports
    import arch.system.state.resource_machine.notes.nockma open;
    import arch.system.state.resource_machine.notes.runnable open;
    import arch.system.state.resource_machine.notes.nockma_runnable open;

    -- Helper Nouns
    zeroNoun : Noun := Noun.Atom 0;
    oneNoun : Noun := Noun.Atom 1;
    keyA : Noun := Noun.Atom 97; -- "a"
    keyB : Noun := Noun.Atom 98; -- "b"
    val3 : Noun := Noun.Atom 3;

    -- Nockma Programs (Executables)

    -- Program to write 3 to key "a" (97)
    -- Nock: [1 [0 [[97 3] 0]]] - Ignores subject, returns constant output.
    writeAOutputNoun : Noun := Noun.Cell (Noun.Atom 0) (Noun.Cell (Noun.Cell keyA val3) zeroNoun);
    writeAProgram : Noun := Noun.Cell oneNoun writeAOutputNoun;

    -- Program to read "a", increment, write to "b"
    -- Nock: [[1 0] [[[1 98] [4 /7]] [1 0]]]
    -- Dynamically builds the output [0 [[98 ++val] 0]] using the subject [state [key val]].
    incWriteProgram : Noun :=
      let
        const0 : Noun := Noun.Cell (Noun.Atom 1) (Noun.Atom 0);
        const98 : Noun := Noun.Cell (Noun.Atom 1) (Noun.Atom 98);
        getVal : Noun := Noun.Cell (Noun.Atom 0) (Noun.Atom 7); -- /7 accesses value from [state [key val]]
        incVal : Noun := Noun.Cell (Noun.Atom 4) getVal; -- [4 /7]
        writePair : Noun := Noun.Cell const98 incVal; -- [[1 98] [4 /7]]
        reqList : Noun := Noun.Cell writePair const0; -- [[[1 98] [4 /7]] [1 0]]
      in Noun.Cell const0 reqList; -- [[1 0] [[[1 98] [4 /7]] [1 0]]]

    -- Engine Configuration and Environment Setup

    -- Define NodeID (can be arbitrary for simulation)
    nodeId : NodeID := PublicKey.Curve25519PubKey "0xSIMNODE";

    -- Shard Engine IDs
    shardAId : EngineID := mkPair (some nodeId) "shardA";
    shardBId : EngineID := mkPair (some nodeId) "shardB";
    mempoolWorkerId : EngineID := mkPair (some nodeId) "mempoolWorker";

    -- Key to Shard Mapping
    keyToShardMap (k : KVSKey) : EngineID :=
      if
        | k == 97 := shardAId -- key "a"
        | k == 98 := shardBId -- key "b"
        | else := shardAId -- Default (should only see a or b)
      ;

    -- Mempool Worker Setup
    -- Use default config/env but override keyToShard mapping
    mempoolWorkerLocalCfg : MempoolWorkerLocalCfg := MempoolWorkerLocalCfg.mk@{ keyToShard := keyToShardMap };
    mempoolWorkerCfg : MempoolWorkerCfg := EngineCfg.mk@{
      node := nodeId;
      name := "mempoolWorker";
      cfg := mempoolWorkerLocalCfg
    };
    mempoolWorkerEnv : MempoolWorkerEnv := mempool_worker_environment_example.mempoolWorkerEnv; -- Start with default empty state
    mempoolWorker : Eng := Eng.MempoolWorker (Engine.mk@{
      cfg := mempoolWorkerCfg;
      env := mempoolWorkerEnv;
      behaviour := mempoolWorkerBehaviour;
    });

    -- Shard Setup (Using default behaviour, customized config/env)
    -- Shards start with empty DAG, initial values handled by findMostRecentWrite logic
    shardACfg : ShardCfg := EngineCfg.mk@{ node := nodeId; name := "shardA"; cfg := ShardLocalCfg.mk };
    shardAEnv : ShardEnv := shard_environment_example.shardEnv;
    shardA : Eng := Eng.Shard (Engine.mk@{ cfg := shardACfg; env := shardAEnv; behaviour := shardBehaviour });

    shardBCfg : ShardCfg := EngineCfg.mk@{ node := nodeId; name := "shardB"; cfg := ShardLocalCfg.mk };
    shardBEnv : ShardEnv := shard_environment_example.shardEnv;
    shardB : Eng := Eng.Shard (Engine.mk@{ cfg := shardBCfg; env := shardBEnv; behaviour := shardBehaviour });

    -- Initial Network State

    -- Node containing all engines
    initialNode : Node := Node.mkNode@{
      engines := Map.fromList [
        mkPair (snd mempoolWorkerId) mempoolWorker;
        mkPair (snd shardAId) shardA;
        mkPair (snd shardBId) shardB
      ]
    };

    -- Transaction Candidates
    txWriteA : TransactionCandidate KVSKey KVSKey Executable := TransactionCandidate.mkTransactionCandidate@{
      label := TransactionLabel.mkTransactionLabel@{ read := [97]; write := [97] }; -- Eager read a, write a
      executable := writeAProgram
    };
    txIncWrite : TransactionCandidate KVSKey KVSKey Executable := TransactionCandidate.mkTransactionCandidate@{
      label := TransactionLabel.mkTransactionLabel@{ read := [97]; write := [98] }; -- Eager read a, write b
      executable := incWriteProgram
    };

    -- Initial Messages (Transaction Requests targeting the Mempool Worker)
    -- Assuming sender is some external client ID (can be none for simplicity here)
    clientSenderId : EngineID := mkPair none "client";

    initialMessages : List (EngineMsg Msg) := [
      EngineMsg.mk@{
        sender := clientSenderId;
        target := mempoolWorkerId;
        mailbox := none;
        msg := Msg.MsgMempoolWorker (MempoolWorkerMsg.TransactionRequest (TransactionRequest.mkTransactionRequest@{ tx := txWriteA; resubmission := none }))
      };
      EngineMsg.mk@{
        sender := clientSenderId;
        target := mempoolWorkerId;
        mailbox := none;
        -- Use the increment transaction
        msg := Msg.MsgMempoolWorker (MempoolWorkerMsg.TransactionRequest (TransactionRequest.mkTransactionRequest@{ tx := txIncWrite; resubmission := none }))
      }
    ];

    -- Initial Network State
    initialNetworkState : NetworkState := NetworkState.mkNetworkState@{
      nodes := Map.singleton nodeId initialNode;
      messages := initialMessages;
      currentTime := left 0;
      incrementId := \{n := n}; -- Dummy ID incrementor
      nextId := nodeId        -- Dummy next ID
    };

    -- Simulation Execution
    -- Run the simulation for 20 steps using the selectFirstMessage strategy.
    simulationResult : List (EngineMsg Msg) := simulate selectFirstMessage initialNetworkState 20;

    -- The `simulationResult` variable now holds the list of messages processed
    -- during the simulation run. Analyzing this list would show the sequence
    -- of lock acquisitions, reads, writes, and acknowledgments.

    -- Final Expected State:
    -- - Key 97 ("a") has value 3 (written by Tx1).
    -- - Key 98 ("b") has value 4 (written by Tx2, incrementing the value 3 read from 'a').


    -- Junk for testing

    initialState : Noun := Noun.Atom 0;
    storage : Storage Nat Nat := emptyStorage;
    initialGas : Nat := 1000;

    -- Input for testing writeAProgram
    externalInput1 : Noun := Noun.Cell (Noun.Atom 0) (Noun.Atom 0); -- Arbitrary input for writeA
    subject1 : Noun := Noun.Cell initialState externalInput1;
    prog1Result : Result String (Pair Noun Nat) := GasState.runGasState (nock storage (Noun.Cell subject1 writeAProgram)) initialGas;

    -- Input for testing incWriteProgram
    externalInput2 : Noun := Noun.Cell (Noun.Atom 97) (Noun.Atom 3); -- Simulate input [key=97, value=3]
    subject2 : Noun := Noun.Cell initialState externalInput2;
    prog2Result : Result String (Pair Noun Nat) := GasState.runGasState (nock storage (Noun.Cell subject2 incWriteProgram)) initialGas;
    ```

This setup defines the necessary components, initial state, and transaction logic using Nockma Nouns. The simulation is executed, and the resulting message trace is stored in `simulationResult`.

