# Fixed Size Type

rseed
nonce

equal

## Fixed size type hierarchy diagram

``` mermaid
---
title: Fixed size type hierarchy
---

classDiagram
    class IFixedSize~T~ {
         <<Interface>>
         +bit_size: Int
         +equal(T, T) -> Bool
    }

    IFixedSize <|-- IArithmetic
    IFixedSize <|-- IHash

    class IHash~T, U~ {
        <<Interface>>
        +hash(T) U
    }

    class IArithmetic~T, U~ {
        <<Interface>>
        +add()
        -sub()
    }
```