theory anoma_environment
imports Main ticker_environment
begin

datatype Env
  = EnvTicker "(TickerLocalState, TickerMsg, TickerMailboxState, TickerTimerHandle) EngineEnvironment"

end
