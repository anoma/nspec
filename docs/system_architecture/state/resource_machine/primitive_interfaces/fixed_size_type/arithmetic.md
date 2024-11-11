# Arithmetic

Arithmetic fixed size type is a type of fixed size that additionally supports addition and subtraction.

``` mermaid

classDiagram
    class FixedSize~T, Arg~ {
         <<Interface>>
         +bit_size: Int
         +new(Arg) T
         +equal(T, T) Bool
    }

    FixedSize <|-- Arithmetic

    class Arithmetic~T, Arg~ {
        <<Interface>>
        +add(T, T) T
        +sub(T, T) T
    }

    Arithmetic <|-- Quantity

```

## Used in
1. Resource component: `quantity`
2. `DeltaHash`

