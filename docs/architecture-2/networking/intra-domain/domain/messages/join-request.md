# JoinRequest


## Purpose


<!-- --8<-- [start:purpose] -->
Request to join a domain.
<!-- --8<-- [end:purpose] -->

## Reception


<!-- --8<-- [start:reception] -->
- Any Local Engine $\to$ [[JoinRequest#joinrequest]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[JoinRequest#joinrequest]] $\to$ [[Domain#domain]]
<!-- --8<-- [end:reception] -->

## Structure


| Field       | Type                  | Description                    |
|-------------|-----------------------|--------------------------------|
| `requestor` | *ExternalIdentity*    | External identity of requestor |
| `domain`    | *ExternalIdentity*    | Domain ID to join              |
| `auth`      | *Option\<Vec\<u8\>\>* | Optional authentication data   |
| `sig`       | *Signature*           | Signature by `requestor`       |

## Triggers


<!-- --8<-- [start:triggers] -->
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ Any Local Engine
<!-- --8<-- [end:triggers] -->
