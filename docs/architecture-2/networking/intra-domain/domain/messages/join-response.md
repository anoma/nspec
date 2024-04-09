# JoinResponse


## Purpose


<!-- --8<-- [start:purpose] -->
Response to a [[JoinRequest#joinrequest]].
<!-- --8<-- [end:purpose] -->

## Reception


<!-- --8<-- [start:reception] -->
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ Any Local Engine
<!-- --8<-- [end:reception] -->

## Structure


| Field       | Type               | Description                                                       |
|-------------|--------------------|-------------------------------------------------------------------|
| `approver`  | *ExternalIdentity* | Identity of approver                                              |
| `requestor` | *ExternalIdentity* | Identity of requestor                                             |
| `domain`    | *ExternalIdentity* | Domain ID to join                                                 |
| `epoch`     | *Option<u32>*      | Current epoch of domain the membership is valid from, if approved |
| `result`    | *Result*           | Join decision: acceptance or refusal                              |
| `sig`       | *Signature*        | Signature by `approver`                                           |

## Effects


The [[JoinResponse#ext-response]] is forwarded to the local engine who sent the [[JoinRequest#joinrequest]].

## Triggers


<!-- --8<-- [start:triggers] -->
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ Any Local Engine
<!-- --8<-- [end:triggers] -->
