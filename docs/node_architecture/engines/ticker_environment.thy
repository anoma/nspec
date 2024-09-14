theory ticker_environment
imports Main
        "prelude"
        ticker_overview
        engine_environment
begin

record TickerLocalState =
  counter :: nat

type_synonym TickerMailboxState = Unit
type_synonym TickerTimerHandle = Unit

fun counter :: "TickerLocalState \<Rightarrow> nat" where
  "counter (| TickerLocalState.counter = counter' |) = counter'"

type_synonym TickerEnvironment =
  "(TickerLocalState, TickerMsg, TickerMailboxState, TickerTimerHandle) EngineEnvironment"

end
