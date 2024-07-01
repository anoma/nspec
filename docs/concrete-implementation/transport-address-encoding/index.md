# Transport address encoding

Transport addresses are encoded as the pair of a natural number identifier (specifying a particular transport) and bytes (an address meaningful to that transport).

```juvix
type TransportAddress := mkTransportAddress {
    transportIdentifier : Natural;
    transportBytes :: []byte;
};
```

| Identifier | Hash function |
| - | - | 
| 0x00 | - (reserved for the future) |
| 0x01 | - (reserved for the future) |