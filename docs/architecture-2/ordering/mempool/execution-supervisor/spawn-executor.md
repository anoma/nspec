# SpawnExecutor

<!-- ANCHOR: blurp -->
- _from_ [[Worker Engine|Worker]]

## Purpose

Informs the supervisor about the need to spawn a new [[Executor]].

<!-- ANCHOR_END: blurp -->
<!-- ANCHOR: details -->

## Structure

| Field   | Type | Description                 |
|---------|------|-----------------------------|
| `spawn` | Unit | no information needed in V1 |

## Effects

A new Executor instance is spawned or (a finished Executor is reused).

## Triggers

- [[ExecutorPIDAssigned]]→[[Worker Engine|Worker]]:  
  send [[ExecutorPIDAssigned]] to the worker that sent the message

<!-- ANCHOR_END: details -->
