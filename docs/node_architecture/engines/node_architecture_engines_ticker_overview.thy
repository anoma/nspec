theory node_architecture_engines_ticker_overview
imports Main
        node_architecture_basics
begin

datatype TickerMsg
  = (* --8<-- [start:Increment] *)
    Increment |
    (* --8<-- [end:Increment] *)
    (* --8<-- [start:Count] *)
    Count

end
