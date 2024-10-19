---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix
- Types
- Network
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.network;
    import node_architecture.types.basics open;
    import node_architecture.types.crypto open;
    import node_architecture.types.identities open;
    import prelude open public;
    ```

# Network Types

## IPv4Address

```juvix
syntax alias IPv4Address := Nat;
```

## IPv6Address

```juvix
syntax alias IPv6Address := Nat;
```

## IPAddress

```juvix
IPAddress : Type := Either IPv4Address IPv6Address;
```

## TODO TransportProtocol 

```juvix
type TransportProtocol : Type :=
  | TCP_Noise
  | UDP_Noise
  | QUIC_TLS
  | QUIC_Noise
  | TLS
  | WebTransport
  | WebSocket
  | TCP
  | UDP
  ;
```

## TLSAddr

```juvix
type TLSAddr : Type :=
  mkTLSAddr {
    --- IP Address
    ip : IPAddress;
    --- Port number
    port : Nat;
    --- TLS certificate issuer fingerprint
    cert_issuer : String;
  };
```

## TransportAddress

```juvix
type TransportAddress : Type :=
  | QUICAddress TLSAddr
  | TLSAddress TLSAddr
  | TorAddress String
  ;
```

## NodeAdvert

The signed *node advertisement* contains the cryptographic identity, transport addresses,
cryptographic keys

```juvix
type NodeAdvert : Type :=
  mkNodeAdvert {
    id : NodeID; 
    addrs : List TransportAddress;
    prekeys : List ExternalID;
    version : Nat;
    created : AbsTime;
    sig : Commitment;
  };
```

`id`
: Node identity.

`addrs`
: Transport addresses with preferences expressed as weights.

`prekeys`
: Prekeys for asynchronous communication.

`version`
: Version number (incremented at every change).

`created`
: Time of creation.

`sig`
: Signature by `id`.

### RoutingPrefs

```juvix
type RoutingPrefs := mkRoutingPrefs {
};
```

### TransportPrefs

```juvix
type TransportPrefs := mkTransportPrefs {
};
```
