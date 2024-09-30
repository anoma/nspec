theory node_architecture_engines_ticker
imports Main
        prelude
        node_architecture_types_engine_family
        node_architecture_engines_ticker_overview
        node_architecture_engines_ticker_environment
        node_architecture_engines_ticker_dynamics
begin

definition TickerEngineFamily :: "(TickerLocalState, TickerMsg, Unit, Unit, TickerMatchableArgument, TickerActionLabel, Unit) node_architecture_types_engine_family.EngineFamily" where
  "TickerEngineFamily = (
    let
      guards' = [incrementGuard, countGuard];
      action' = tickerAction;
      conflictSolver' = tickerConflictSolver
    in (| EngineFamily.guards = guards', EngineFamily.action = action', EngineFamily.conflictSolver = conflictSolver' |))"

end
