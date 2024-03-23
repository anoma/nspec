# ExtResponse

## Purpose

<!-- ANCHOR: purpose -->
External request to a domain.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- [[Domain#domain]] $\to$ [[ExtResponse#extrequest]] $\to$ [[Domain#domain]]
<!-- ANCHOR_END: reception -->

## Structure

Defined by domain protocols.

## Effects

The [[ExtResponse#ext-response]] is forwarded to the local engine who sent the [[ExtRequest#extrequest]].

## Triggers

<!-- ANCHOR: triggers -->
- [[Domain#domain]] $\to$ [[ExtResponse#extresponse]] $\to$ Any Local Engine
<!-- ANCHOR_END: triggers -->
