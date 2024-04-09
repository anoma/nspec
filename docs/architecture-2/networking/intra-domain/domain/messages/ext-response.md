# ExtResponse

## Purpose

<!-- --8<-- [start:purpose] -->
External request to a domain.
<!-- --8<-- [end:purpose] -->

## Reception

<!-- --8<-- [start:reception] -->
- [[Domain#domain]] $\to$ [[ExtResponse#extrequest]] $\to$ [[Domain#domain]]
<!-- --8<-- [end:reception] -->

## Structure

Defined by domain protocols.

## Effects

The [[ExtResponse#ext-response]] is forwarded to the local engine who sent the [[ExtRequest#extrequest]].

## Triggers

<!-- --8<-- [start:triggers] -->
- [[Domain#domain]] $\to$ [[ExtResponse#extresponse]] $\to$ Any Local Engine
<!-- --8<-- [end:triggers] -->
