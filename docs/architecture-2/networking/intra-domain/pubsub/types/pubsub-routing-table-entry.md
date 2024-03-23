# PubSubRoutingTableEntry

## Purpose

A pub/sub routing table entry.

## Type

A *struct* with the following fields:

| Field      | Type                              | Description                                                 |
|------------|-----------------------------------|-------------------------------------------------------------|
| `id`       | *[[TopicIdentity#topicidentity]]* | Topic ID                                                    |
| `advert`   | *[[TopicAdvert#topicadvert]]*     | Topic advertisement                                         |
| `parents`  | *[[NodeIdentity#nodeidentity]]*   | Parent peers incoming messages arrive from for the topic    |
| `children` | *[[NodeIdentity#nodeidentity]]*   | Children peers to forward incoming messages to in the topic |
