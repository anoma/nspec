# BlockLookupRequest


## Purpose


<!-- --8<-- [start:purpose] -->
Look up a block in local storage and on the network.
<!-- --8<-- [end:purpose] -->

## Reception


<!-- --8<-- [start:reception] -->
- Any Local Engine $\to$ *BlockLookupRequest* $\to$ Storage
<!-- --8<-- [end:reception] -->

## Structure


| Field    | Type                                          | Description                          |
|----------|-----------------------------------------------|--------------------------------------|
| `block`  | *[[BlockId#blockid]]*                         | Block ID                             |
| `topic`  | *Option\<[[TopicIdentity#topicidentity]]\>*   | Enable search in a PubSub topic      |
| `random` | *bool*                                        | Enable search using random walk      |
| `domain` | *Option\<[[DomainIdentity#domainidentity]]\>* | Restrict the random walk to a domain |

## Behavior


First query the local storage for the block.
If not found, initiate a search on the network, when either `topic` or `random` is enabled.

## Triggers


<!-- --8<-- [start:triggers] -->
- Storage $\to$ *[[BlockResponse#blockresponse]]* $\to$ Any Local Engine
<!-- --8<-- [end:triggers] -->
