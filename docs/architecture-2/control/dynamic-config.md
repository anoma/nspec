<div class="engine" markdown>


# Dynamic Configuration Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The *Dynamic Configuration Engine* stores dynamic configurations of the engines and notifies them about configuration changes.
Unlike the *Static Configuration Engine*, the *Dynamic Configuration Engine* allows engines to modify the configuration at runtime. 
<!-- --8<-- [end:purpose] -->

## State


## Messages Received

### [[GetDynamicConfigRequest#getdynamicconfigrequest]]

--8<-- "dynamic-config-engine/messages/get-dynamic-config-request.md:purpose"

--8<-- "dynamic-config-engine/messages/get-dynamic-config-request.md:type"

### [[SetDynamicConfigRequest#setdynamicconfigrequest]]

--8<-- "dynamic-config-engine/messages/set-dynamic-config-request.md:purpose"

--8<-- "dynamic-config-engine/messages/set-dynamic-config-request.md:type"

### [[DeleteDynamicConfigRequest#deletedynamicconfigrequest]]

--8<-- "dynamic-config-engine/messages/delete-dynamic-config-request.md:purpose"

--8<-- "dynamic-config-engine/messages/delete-dynamic-config-request.md:type"

### [[SubscribeDynamicConfigRequest#subscribedynamicconfigrequest]]

--8<-- "dynamic-config-engine/messages/subscribe-dynamic-config-request.md:purpose"

--8<-- "dynamic-config-engine/messages/subscribe-dynamic-config-request.md:type"


## Notifications Sent

### [[DynamicConfigChanged#dynamicconfigchanged]]

--8<-- "dynamic-config-engine/notifications/dynamic-config-changed.md:purpose"

--8<-- "dynamic-config-engine/notifications/dynamic-config-changed.md:type"


## Message Flow

<!-- --8<-- [start:messages] -->

```mermaid

sequenceDiagram

--8<-- "dynamic-config-engine/messages/get-dynamic-config-request.md:sequence"
--8<-- "dynamic-config-engine/messages/set-dynamic-config-request.md:sequence"
--8<-- "dynamic-config-engine/messages/delete-dynamic-config-request.md:sequence"
--8<-- "dynamic-config-engine/messages/subscribe-dynamic-config-request.md:sequence"


```

<!-- --8<-- [end:messages] -->

</div>
