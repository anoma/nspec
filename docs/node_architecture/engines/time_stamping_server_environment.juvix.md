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
    module node_architecture.engines.time_stamping_server_environment;
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
the latter may shut down in case
they do not receive any requests for a certain period of time.

## Messages  

??? note "Auxiliary Juvix code"

    ```juvix
    TimeStampingHash : Type := Nat;
    TimeStampingID : Type := String;
    ```
    
    
```juvix 
type TimeStampingServerMessage :=     
  | -- --8<-- [start:requestTimeStamp]
    requestTimeStamp {
        hash : TimeStampingHash ;
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
    module request_time_stamp_example;
        request : TimeStampingServerMessage := requestTimeStamp@{
            hash := 0;
            destination := "Bob"
        };
    end;
```

hash

:   The hash is the hash to be stamped.

destination

:   The destination describes the intended recipient of
    the time stamped hash.

## Mailbox states 

??? note "Auxiliary Juvix code"

    ```juvix
    -- no auxiliary definitions
    ```

```juvix
type TimeStampingServerMailboxState :=
     -- --8<-- [start:rateLimit]
     rateLimit {
         limit : Nat ;
         timeStamps : List Nat
     };
     -- --8<-- [end:rateLimit]
```

### rateLimit

!!! quote ""

    --8<-- "./time_stamping_server_environment.juvix.md:rateLimit"

Besides the fixed rate limit (of a mailbox),
we keep track of the time stamps of previous requests.

limit 

:   The limit gives the rate limit in requests per second
    for the respective mailbox.

timeStamps

:   This is a list of the time stamps of previous requests (received recently).

## Local state

```juvix
type TimeStampingServerLocalState :=
    -- --8<-- [start:globalLimit]
    globalLimit{
        limit : Nat ;
        auxiliary : Bool
    };
    -- --8<-- [start:globalLimit]
```

## Timer handles

```juvix
type TimeStampingServerTimerHandle :=
     | timeToShutDown String;
```

Auxiliary engines set this timer
to be notified when it is time to shut down
(unless there was a recent request).

## Environment summary 

```juvix
TimeStampingServerEnvironment : Type :=
  EngineEnvironment
    TimeStampingServerLocalState
    TimeStampingServerMessage
    TimeStampingServerMailboxState
    TimeStampingServerTimerHandle;
```


```juvix
    module time_stamping_server_environment_example;
    import node_architecture.basics open;
    env : TimeStampingServerEnvironment := mkEngineEnvironment@{
        name := Left "Server";
        localState := globalLimit@{limit := 100; auxiliary := false};
        mailboxCluster := Map.empty;
        acquaintances := Set.empty;
        timers := [];
    };
    end;
```

