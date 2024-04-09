# EventV1


## Purpose


<!-- --8<-- [start:purpose] -->
Describe the purpose of the type.
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
<div class="type" markdown>


*Record* with fields:

- `topic`: [[TopicIdentity#topicidentity]]

  *Topic the event is published to*

- `publisher`: [[EngineIdentity#engineidentity]]

  *PubSub engine identity of pulisher*

- `seq`: u32

  *Sequence number of publisher*

- `deps`: Vec\<EventId\>

  *Events this event depends on*

- `seen`: Vec\<EventId\>

  *Independent events recently seen*

- `body`: Vec\<u8\>

  *Encapsulated [[EngineMessage#enginemessage]]*

- `sig`: [[Signature#signature]]

  *Signature by `publisher` over the above fields*

</div>
<!-- --8<-- [end:type] -->
