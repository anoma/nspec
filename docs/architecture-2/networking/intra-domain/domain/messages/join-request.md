# JoinRequest

## Purpose

<!-- ANCHOR: purpose -->
Request to join a domain.
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- Any Local Engine $\to$ [[JoinRequest#joinrequest]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[JoinRequest#joinrequest]] $\to$ [[Domain#domain]]
<!-- ANCHOR_END: reception -->

## Structure

| Field       | Type                  | Description                    |
|-------------|-----------------------|--------------------------------|
| `requestor` | *ExternalIdentity*    | External identity of requestor |
| `domain`    | *ExternalIdentity*    | Domain ID to join              |
| `auth`      | *Option\<Vec\<u8\>\>* | Optional authentication data   |
| `sig`       | *Signature*           | Signature by `requestor`       |

## Triggers

<!-- ANCHOR: triggers -->
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ Any Local Engine
<!-- ANCHOR_END: triggers -->
