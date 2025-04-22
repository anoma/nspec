---
icon: material/tools
search:
  exclude: false
tags:
  - node-architecture
  - utils
  - engine
---

??? code "Juvix imports"

    ```juvix
    module arch.node.utils;

    import prelude open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;
    ```

# Utility Functions for Engine Behavior

This module provides generic utility functions to simplify common patterns in engine behaviors,
particularly for creating message responses and action effects. These utilities are designed to
work with any engine type without requiring engine-specific customization.

## Message Construction Utilities

### `createReplyMsg`

Creates a standard engine message reply based on the incoming message, with a specified reply message content.

<!-- --8<-- [start:createReplyMsg] -->
```juvix
defaultReplyMsg
  {M C}
  (cfg : EngineCfg C)
  (target : EngineID)
  (replyMsg : M)
  : EngineMsg M :=
    mkEngineMsg@{
      sender := getEngineIDFromEngineCfg cfg;
      target := target;
      mailbox := some 0;
      msg := replyMsg
    };
```
<!-- --8<-- [end:createReplyMsg] -->

## Action Effect Utilities

### `msgActionEffect`

Creates an action effect specifically for Anoma message types, handling the conversion between specific configuration types and the PreCfg type.

<!-- --8<-- [start:msgActionEffect] -->
```juvix
msgActionEffect
  {S B H}
  (env : EngineEnv S B H Anoma.Msg)
  (msgs : List (EngineMsg Anoma.Msg))
  : ActionEffect S B H Anoma.Msg Anoma.Cfg Anoma.Env :=
    mkActionEffect@{
      env := env;
      msgs := msgs;
      timers := [];
      engines := []
    };
```
<!-- --8<-- [end:msgActionEffect] -->

### `replyActionEffect`

Creates an action effect with a single reply message specifically for Anoma message types.

<!-- --8<-- [start:replyActionEffect] -->
```juvix
replyActionEffect
  {S B H C}
  (env : EngineEnv S B H Anoma.Msg)
  (cfg : EngineCfg C)
  (target : EngineID)
  (replyMsg : Anoma.Msg)
  : ActionEffect S B H Anoma.Msg Anoma.Cfg Anoma.Env :=
    let
      msg := defaultReplyMsg cfg target replyMsg
    in msgActionEffect {S} {B} {H} env [msg];
```
<!-- --8<-- [end:replyActionEffect] -->

### `defaultReplyActionEffect`

Creates an action effect with a single reply message using the default mailbox (ID 0) specifically for Anoma message types.

<!-- --8<-- [start:defaultReplyActionEffect] -->
```juvix
defaultReplyActionEffect
  {S B H C}
  (env : EngineEnv S B H Anoma.Msg)
  (cfg : EngineCfg C)
  (target : EngineID)
  (replyMsg : Anoma.Msg)
  : ActionEffect S B H Anoma.Msg Anoma.Cfg Anoma.Env :=
    replyActionEffect {S} {B} {H} {C} env cfg target replyMsg;
```
<!-- --8<-- [end:defaultReplyActionEffect] -->
