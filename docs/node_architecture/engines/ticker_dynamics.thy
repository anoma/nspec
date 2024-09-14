theory ticker_dynamics
imports Main
        basics
        engine_family
        ticker_overview
        ticker_environment
begin

datatype GuardReturnLabel
  = doIncrement |
    doRespond nat

datatype GuardReturnArgs
  = ReplyTo "((string, nat) Either) option" "nat option"

datatype GuardReturnOther
  = nuthing

fun ifIncrement :: "nat option \<Rightarrow> (TickerMsg, TickerTimerHandle) Trigger \<Rightarrow> (TickerLocalState, TickerMsg, TickerMailboxState, TickerTimerHandle) EngineEnvironment \<Rightarrow> ((GuardReturnArgs, GuardReturnLabel, GuardReturnOther) GuardOutput) option" where
  "ifIncrement v (MessageArrived m) v' =
    (case getMessageType m of
       Increment \<Rightarrow>
         Some (let
                 args' = [];
                 label' = doIncrement;
                 other' = nuthing
               in (| GuardOutput.args = args', GuardOutput.label = label', GuardOutput.other = other' |)) |
       v'0 \<Rightarrow> None)" |
  "ifIncrement v (Elapsed ts ) v' = None"

end
