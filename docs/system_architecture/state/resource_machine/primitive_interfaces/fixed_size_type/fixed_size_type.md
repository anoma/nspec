# Fixed Size Type

Fixed size type is a type, as the name suggests, of a fixed size. An example of such a type could be a prime field, unit32, or a string of a fixed size. An example of a type of not fixed size would be a list<uint32>. All resource components and computable components are elements of a fixed size type.

The two child interfaces are *arithmetic fixed size type* - the fixed size type that supports addition and subtraction, and *hash* - the fixed size type for which the type derivation function `new(Arg)` is *binding*.

## Fixed size type hierarchy diagram

``` mermaid

classDiagram
    class FixedSize~T, Arg~ {
         <<Interface>>
         +bit_size: Int
         +new(Arg) T
         +equal(T, T) Bool
    }

    FixedSize <|-- Nonce
    FixedSize <|-- RandSeed
    FixedSize <|-- NullifierKeyCommitment
    FixedSize <|-- NullifierKey

    FixedSize <|-- Arithmetic
    FixedSize <|-- Hash


    note for Hash "fixed size types that are binding (to Arg) and collision resistant"
    class Hash~T, Arg~ {
        <<Interface>>
    }

    class Arithmetic~T, Arg~ {
        <<Interface>>
        +add(T, T) T
        +sub(T, T) T
    }

    Hash <|-- DeltaHash
    Arithmetic <|-- DeltaHash

    note for DeltaHash "additively homomorphic and kind-distnict"
    class DeltaHash {
        <<Interface>>
    }

```

## Used in (raw)

- rseed, nonce, cnk, nullifierKey