theory node_architecture_types_anoma_environment
imports Main
        node_architecture_engines_ticker_environment
begin

datatype Env
  = EnvTicker "(TickerLocalState, TickerMsg, Unit, Unit) EngineEnvironment"

end
