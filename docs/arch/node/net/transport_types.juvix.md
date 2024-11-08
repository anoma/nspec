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
    module arch.node.net.transport_types;

    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import prelude open;
    ```

# Transport types

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

## TransportProtocol

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

## TLSAddress

```juvix
type TLSAddress :=
  mkTLSAddress {
    ip : IPAddress;
    port : Nat;
    cert_issuer : String;
  };
```

`ip`
: IP address

`port`
: Port number

`cert_issuer`
: TLS certificate issuer fingerprint

## TransportAddress

```juvix
type TransportAddress :=
  | QUICAddr TLSAddress
  | TLSAddr TLSAddress
  | IPAddr IPAddress
  ;
```

## TransportOrderingPrefs

Transport ordering preferences for an outgoing message.

```juvix
type TransportOrderingPrefs :=
  | TransportOrdered
  | TransportUnordered
  ;
```

## TransportReliabilityPrefs

Transport reliability preferences for an outgoing message.

```juvix
type TransportReliabilityPrefs :=
  | TransportReliable
  | TransportUnreliable
  ;
```

## TransportSecurityPrefs

Transport ordering preferences for an outgoing message.

```juvix
type TransportSecurityPrefs :=
  | TransportDirect
  ;
```

## TransportPrefs

Transport preferences for an outgoing message.

```juvix
type TransportPrefs := mkTransportPrefs {
  ordering : TransportOrderingPrefs;
  reliability : TransportReliabilityPrefs;
  security : TransportSecurityPrefs;
};
```

`ordering`
:	Transport ordering preferences

`reliability`
:	Transport reliability preferences

`security`
: Transport security preferences
