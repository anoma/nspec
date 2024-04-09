# KVSKey

## Purpose

The datatype for keys of RSM state.

## Structure

This is a basic type and thus could be a parameter.
In V1, the default is a 256-bit hash.

## Note

If $n$ shards are used, for $n\in \mathbb{N}$,
then shard $i$ will be responsible for a key $k$
if, and only if, $k \equiv i \mod n$.
