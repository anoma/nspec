theory anoma_message
imports Main
        basics
        ticker_overview
begin

datatype Msg
  = MsgTicker TickerMsg

end
