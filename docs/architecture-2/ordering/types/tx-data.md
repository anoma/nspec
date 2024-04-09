# TxData


## Purpose


We define _TxData_ as an alias for
a string of bytes that contains all relevant data of a
[[TransactionCandidate|transaction candidate]].
<!--
It is in particular used in the context of certificates of availability.
-->

## Structure


This is a basic type and could be a type parameter.
The default is a byte string, e.g.,
[binary](
https://hexdocs.pm/elixir/binaries-strings-and-charlists.html#binaries)
in Elixir.
