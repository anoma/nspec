theory node_architecture_types_anoma_message
imports Main
        node_architecture_basics
        node_architecture_engines_ticker_overview
begin

datatype Msg
  = MsgTicker TickerMsg

end
