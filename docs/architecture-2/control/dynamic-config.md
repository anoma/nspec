<div class="engine">

# Dynamic Configuration Engine

## Purpose

<!-- ANCHOR: purpose -->
The *Dynamic Configuration Engine* stores dynamic configurations of the engines and notifies them about configuration changes.
Unlike the *Static Configuration Engine*, the *Dynamic Configuration Engine* allows engines to modify the configuration at runtime. 
<!-- ANCHOR_END: purpose -->

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

 <!-- ANCHOR: messages -->

 ```mermaid

 sequenceDiagram

 {{#include dynamic-config-engine/messages/get-dynamic-config-request.md:sequence}}
 {{#include dynamic-config-engine/messages/set-dynamic-config-request.md:sequence}}
 {{#include dynamic-config-engine/messages/delete-dynamic-config-request.md:sequence}}
 {{#include dynamic-config-engine/messages/subscribe-dynamic-config-request.md:sequence}}


 ```

 <!-- ANCHOR_END: messages -->

</div>
