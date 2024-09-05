--- 
icon: octicons/gear-16  
search:
  exclude: false
categories:
- engine-family 
- juvix-module
tags:
- tutorial
- engine-environment
---

??? note "Juvix preamble"

    ```juvix
    module tutorial.engines.template.time_stamping_server_environment;
    import prelude open;
    import node_architecture.types.engine_family open;
    ```

# Time Stamping Server Environment 

## Overview 

Time stampers have rate limits.
The rate limits come in two variations:
relative to mailboxes
and in summary for the whole server.
If the total load of the server is too high,
new "auxiliary" time stamping servers will be spawned;
the later may shut down
when their load is low.

## Messages  


??? note "Auxiliary Juvix code"

    ```
    syntax alias TimeStampingHash := String;
    syntax alias TimeStampingID := String;
    ```

```juvix 
type TimeStampingServerMessage :=     
  | -- --8<-- [start:requestTimeStamp]
    requestTimeStamp {
        hash : TimeStampingHash;
        destination : TimeStampingID
    };
  -- --8<-- [end:requestTimeStamp]
``` 

### requestTimeStamp

!!! quote ""

    --8<-- "./time_stamping_server_environment.juvix.md:requestTimeStamp"

This message is sent by a TimeStampingClient engine
whenever it is in need of a hash to be time stamped
by the receiving time stamper.

```juvix
    module requestTimeStampExample;
        request : TimeStampingServerMessage := requestTimeStamp@{
            hash := 0;
            destination := 0
        };
    end;
```

### [Message constructor ...]

[...] 

## Mailbox states 

??? note "Auxiliary Juvix code 

    [...]

[...]  

## Local state 

[...] 

## Timer handles 

??? note "Auxiliary Juvix code"

    [...] 

[...] 

## Environment summary 

[...]
