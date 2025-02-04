---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - node-architecture
  - types
  - network-subsystem
  - transport
  - prelude
---

??? code "Juvix imports"

    ```juvix
    module arch.node.types.transport;

    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    ```

# Transport types

## `IPv4Address`

```juvix
syntax alias IPv4Address := Nat;
```

## `IPv6Address`

```juvix
syntax alias IPv6Address := Nat;
```

## `IPAddress`

```juvix
IPAddress : Type := Either IPv4Address IPv6Address;
```

## `TransportProtocol`

Supported network transport protocols.

```juvix
type TransportProtocol :=
  | QUIC
  | TLS
  | WebTransport
  | WebSocket
  | TCP
  | UDP
  ;
```

## `TLSAddress`

TLS or QUIC address.

```juvix
type TLSAddress :=
  mkTLSAddress {
    ip : IPAddress;
    port : Nat;
    cert_issuer : String;
  };
```


???+ code "Arguments"

    `ip`
    : IP address

    `port`
    : Port number

    `cert_issuer`
    : TLS certificate issuer fingerprint

## `TransportAddress`

```juvix
type TransportAddress :=
  | QUICAddr TLSAddress
  | TLSAddr TLSAddress
  | IPAddr IPAddress
  ;
```

## `TransportOrderingPrefs`

Transport ordering preferences for an outgoing message.

```juvix
type TransportOrderingPrefs :=
  | TransportOrdered
  | TransportUnordered
  ;
```

## `TransportReliabilityPrefs`

Transport reliability preferences for an outgoing message.

```juvix
type TransportReliabilityPrefs :=
  | TransportReliable
  | TransportUnreliable
  ;
```

## `TransportSecurityPrefs`

Transport ordering preferences for an outgoing message.

```juvix
type TransportSecurityPrefs :=
  | TransportDirect
  ;
```

## `TransportPrefs`

Transport preferences for an outgoing message.

```juvix
type TransportPrefs := mkTransportPrefs {
  ordering : TransportOrderingPrefs;
  reliability : TransportReliabilityPrefs;
  security : TransportSecurityPrefs;
};
```

???+ code "Arguments"

    `ordering`
    :	Transport ordering preferences

    `reliability`
    :	Transport reliability preferences

    `security`
    : Transport security preferences

## `SerializedMsg`

Serialized message.
Contains an `EngineMsg`.

<!-- --8<-- [start:SerializedMsg] -->
```juvix
type SerializedMsg :=
  | BARE ByteString
  ;
```
<!-- --8<-- [end:SerializedMsg] -->

???+ code "Arguments"

    `SerializedMsgBARE`
    : BARE

## `EncryptedMsg`

Serialized message encrypted with the specified algorithm.
Contains a `SerializedMsg`.

<!-- --8<-- [start:EncryptedMsg] -->
```juvix
type EncryptedMsg :=
  | EncryptedMsgNull ByteString
  ;
```
<!-- --8<-- [end:EncryptedMsg] -->

???+ code "Arguments"

    `EncryptedMsgNull`
    : No encryption.
