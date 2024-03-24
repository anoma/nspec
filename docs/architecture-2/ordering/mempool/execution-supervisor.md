# Execution Supervisor

## Purpose

The execution supervisor in V1 is essentially the engine counterpart
to the Erlang or Elixir `spawn`-command
(for a process waiting for [[ExecuteTransaction]]-commands).
This will be more complicated in future versions
where a single transaction might be processed
by geo-distributed executors to allow for collocation with shards.


## [[SpawnExecutor]]

--8<-- "./execution-supervisor/spawn-executor.md:blurp"
<details>
    <summary>Details</summary>
--8<-- "./execution-supervisor/spawn-executor.md:details"
</details>



