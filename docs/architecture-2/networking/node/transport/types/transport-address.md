# TransportAddress

## Purpose

A transport address.

## Type

One of the following types, depending on the transport protocol.

- QUICAddr
- WSSAddr
- TorAddr
- VeilidAddr
- ...

### QUICAddr & WSSAddr

For transports over IP that use X.509 certificates (such as QUIC & Secure WebSocket),
the destination IP address & port, as well as the certificate issuer public key is given.
The latter is used to verify the transport certificate of the remote peer.

| Field         | Type                                    | Description                   |
|---------------|-----------------------------------------|-------------------------------|
| `ip`          | *[[IPAddress#ipaddress]]*               | IP Address                    |
| `port`        | *u16*                                   | Port number                   |
| `cert_issuer` | *[[ExternalIdentity#externalidentity]]* | Certificate issuer public key |

#### TorAddr & VeilidAddr

For transports that use public key addressing (such as Tor & Veilid),
the destination public key address is given,
possibly together with additional transport-specific dial information.

| Field  | Type        | Description |
|--------|-------------|-------------|
| `addr` | *Vec\<u8\>* | Address     |
