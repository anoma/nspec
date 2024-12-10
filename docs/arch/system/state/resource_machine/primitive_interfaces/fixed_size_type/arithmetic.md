# Arithmetic

Arithmetic fixed size type is a type of fixed size that additionally supports addition and subtraction.

<!--ᚦ«a quick note on commutativity would not hurt, IMHO»-->

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
    Arithmetic <|-- Balance

```

## Used in
1. Resource component: `quantity`
2. `DeltaHash`

<!--ᚦ«links would be nice»-->
<!--ᚦ«balance should probably also be on this list»-->
