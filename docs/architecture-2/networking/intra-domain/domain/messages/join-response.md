# JoinResponse

## Purpose

<!-- ANCHOR: purpose -->
Response to a [[JoinRequest#joinrequest]].
<!-- ANCHOR_END: purpose -->

## Reception

<!-- ANCHOR: reception -->
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ [[Domain#domain]]
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ Any Local Engine
<!-- ANCHOR_END: reception -->

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

<!-- ANCHOR: triggers -->
- [[Domain#domain]] $\to$ [[JoinResponse#joinresponse]] $\to$ Any Local Engine
<!-- ANCHOR_END: triggers -->
