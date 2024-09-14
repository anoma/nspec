theory ticker
imports Main
        "prelude"
        "ticker_overview"
        "ticker_environment"
        "ticker_dynamics"
        "engine_family"
begin

type_synonym TickerEngineFamily =
      "(TickerLocalState,
        TickerMsg,
        TickerMailboxState,
        TickerTimerHandle,
        Unit,
        Unit,
        Unit) EngineFamily"

end
