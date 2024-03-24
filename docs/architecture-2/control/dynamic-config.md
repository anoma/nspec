<div class="engine">

# Dynamic Configuration Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The *Dynamic Configuration Engine* stores dynamic configurations of the engines and notifies them about configuration changes.
Unlike the *Static Configuration Engine*, the *Dynamic Configuration Engine* allows engines to modify the configuration at runtime. 
<!-- --8<-- [end:purpose] -->

## State


## Messages Received

### [[GetDynamicConfigRequest#getdynamicconfigrequest]]

{{#include dynamic-config-engine/messages/get-dynamic-config-request.md:purpose}}

{{#include dynamic-config-engine/messages/get-dynamic-config-request.md:type}}

### [[SetDynamicConfigRequest#setdynamicconfigrequest]]

{{#include dynamic-config-engine/messages/set-dynamic-config-request.md:purpose}}

{{#include dynamic-config-engine/messages/set-dynamic-config-request.md:type}}

### [[DeleteDynamicConfigRequest#deletedynamicconfigrequest]]

{{#include dynamic-config-engine/messages/delete-dynamic-config-request.md:purpose}}

{{#include dynamic-config-engine/messages/delete-dynamic-config-request.md:type}}

### [[SubscribeDynamicConfigRequest#subscribedynamicconfigrequest]]

{{#include dynamic-config-engine/messages/subscribe-dynamic-config-request.md:purpose}}

{{#include dynamic-config-engine/messages/subscribe-dynamic-config-request.md:type}}


## Notifications Sent

### [[DynamicConfigChanged#dynamicconfigchanged]]

{{#include dynamic-config-engine/notifications/dynamic-config-changed.md:purpose}}

{{#include dynamic-config-engine/notifications/dynamic-config-changed.md:type}}


## Message Flow
![]

 <!-- --8<-- [start:messages] -->

 ```mermaid

 sequenceDiagram

 {{#include dynamic-config-engine/messages/get-dynamic-config-request.md:sequence}}
 {{#include dynamic-config-engine/messages/set-dynamic-config-request.md:sequence}}
 {{#include dynamic-config-engine/messages/delete-dynamic-config-request.md:sequence}}
 {{#include dynamic-config-engine/messages/subscribe-dynamic-config-request.md:sequence}}


 ```

 <!-- --8<-- [end:messages] -->

</div>
