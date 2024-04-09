<div class="message" markdown>


# GetStaticConfigRequest


## Purpose


<!-- --8<-- [start:purpose] -->
Find a static configuration by its key in the static configuration KV-store and return it.
<!-- --8<-- [end:purpose] -->

## Type


<!-- --8<-- [start:type] -->
**Reception:**

[[GetStaticConfigRequestV1#getstaticconfigrequestv1]]

--8<-- "../types/get-static-config-request-v1.md:type"

**Triggers**

[[GetStaticConfigResponseV1#getstaticconfigresponsev1]]

--8<-- "../types/get-static-config-response-v1.md:type"

<!-- --8<-- [end:type] -->

## Behavior


<!-- --8<-- [start:behavior] -->
Performs the requested search operation in the static configurations KV-store and returns the value.
<!-- --8<-- [end:behavior] -->


## Message Flow


<!-- --8<-- [start:messages] -->
```mermaid
sequenceDiagram

%% --8<-- [start:sequence]
User ->>+ Static Config Engine: GetStaticConfigRequest
Static Config Engine -->>- User: GetStaticConfigResponse
%% --8<-- [end:sequence]
```

<!-- --8<-- [end:messages] -->

</div>
