theory node_architecture_engines_ticker_environment
imports Main
        prelude
        node_architecture_engines_ticker_overview
        node_architecture_types_engine_environment
begin

record TickerLocalState =
  counter :: nat

fun counter :: "TickerLocalState \<Rightarrow> nat" where
  "counter (| TickerLocalState.counter = counter' |) = counter'"

type_synonym TickerEnvironment = "(TickerLocalState, TickerMsg, Unit, Unit) EngineEnvironment"

definition tickerEnvironmentExample :: TickerEnvironment where
  "tickerEnvironmentExample =
    let
      name' = Left ''ticker'';
      localState' = let
                      counter' = 0
                    in (| TickerLocalState.counter = counter' |);
      mailboxCluster' = Data_Map.empty;
      acquaintances' = Data_Set_AVL.empty;
      timers' = []
    in (| EngineEnvironment.name = name', EngineEnvironment.localState = localState', EngineEnvironment.mailboxCluster = mailboxCluster', EngineEnvironment.acquaintances = acquaintances', EngineEnvironment.timers = timers' |)"

end
