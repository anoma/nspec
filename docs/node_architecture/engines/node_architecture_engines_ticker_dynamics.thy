theory node_architecture_engines_ticker_dynamics
imports Main
        prelude
        node_architecture_basics
        node_architecture_types_engine_family
        node_architecture_engines_ticker_overview
        node_architecture_engines_ticker_environment
        node_architecture_types_engine_environment
        node_architecture_types_engine_dynamics
        node_architecture_types_anoma_message
begin

datatype TickerActionLabel
  = (* --8<-- [start:DoIncrement] *)
    DoIncrement |
    (* --8<-- [end:DoIncrement] *)
    (* --8<-- [start:DoRespond] *)
    DoRespond

(* --8<-- [end:DoRespond] *)
datatype TickerMatchableArgument
  = (* --8<-- [start:ReplyTo] *)
    ReplyTo "((string, nat) Either) option" "nat option"

(* --8<-- [end:ReplyTo] *)
(* --8<-- [start:ticker-guard] *)
type_synonym TickerGuard =
  "(TickerLocalState, TickerMsg, Unit, Unit, TickerMatchableArgument, TickerActionLabel, Unit) Guard"

(* --8<-- [end:ticker-guard] *)
(* --8<-- [start:ticker-guard-output] *)
type_synonym TickerGuardOutput = "(TickerMatchableArgument, TickerActionLabel, Unit) GuardOutput"

(* --8<-- [end:ticker-guard-output] *)
fun incrementGuard :: "(TickerMsg, Unit) TimestampedTrigger \<Rightarrow> (TickerLocalState, TickerMsg, Unit, Unit) EngineEnvironment \<Rightarrow> TickerGuardOutput option" where
  "incrementGuard t env' =
    (case getMessageFromTimestampedTrigger t of
       (Some Increment) \<Rightarrow>
         Some (let
                 args' = [];
                 label' = DoIncrement;
                 other' = unit
               in (| GuardOutput.args = args', GuardOutput.label = label', GuardOutput.other = other' |)) |
       v \<Rightarrow> None)"

fun countGuard :: "(TickerMsg, Unit) TimestampedTrigger \<Rightarrow> (TickerLocalState, TickerMsg, Unit, Unit) EngineEnvironment \<Rightarrow> TickerGuardOutput option" where
  "countGuard t env' =
    (case getMessageFromTimestampedTrigger t of
       (Some Count) \<Rightarrow>
         option_bind (getMessageSenderFromTimestampedTrigger t) (\<lambda> x0 . Some (let
                                                                                                             args' = [ReplyTo (Some x0) None];
                                                                                                             label' = DoRespond;
                                                                                                             other' = unit
                                                                                                           in (| GuardOutput.args = args', GuardOutput.label = label', GuardOutput.other = other' |))) |
       v \<Rightarrow> None)"

type_synonym TickerActionInput =
  "(TickerLocalState, TickerMsg, Unit, Unit, TickerMatchableArgument, TickerActionLabel, Unit) ActionInput"

type_synonym TickerActionEffect =
  "(TickerLocalState, TickerMsg, Unit, Unit, TickerMatchableArgument, TickerActionLabel, Unit) ActionEffect"

fun tickerAction :: "(TickerLocalState, TickerMsg, Unit, Unit, TickerMatchableArgument, TickerActionLabel, Unit) ActionInput \<Rightarrow> TickerActionEffect" where
  "tickerAction input =
    (let
       env' = node_architecture_types_engine_dynamics.env input;
       out = node_architecture_types_engine_dynamics.guardOutput input
     in case node_architecture_types_engine_dynamics.label out of
          DoIncrement \<Rightarrow>
            let
              counterValue = node_architecture_engines_ticker_environment.counter (node_architecture_types_engine_environment.localState env')
            in let
                 newEnv' = env' (| EngineEnvironment.localState := let
                                                                     counter' = counterValue + 1
                                                                   in (| TickerLocalState.counter = counter' |) |);
                 producedMessages' = [];
                 timers' = [];
                 spawnedEngines' = []
               in (| ActionEffect.newEnv = newEnv', ActionEffect.producedMessages = producedMessages', ActionEffect.timers = timers', ActionEffect.spawnedEngines = spawnedEngines' |) |
          DoRespond \<Rightarrow> (
            let
              counterValue = node_architecture_engines_ticker_environment.counter (node_architecture_types_engine_environment.localState env')
            in case node_architecture_types_engine_dynamics.args out of
                 (ReplyTo (Some whoAsked) mailbox' # v) \<Rightarrow>
                   let
                     newEnv' = env';
                     producedMessages' = [let
                                            sender' = getMessageTargetFromTimestampedTrigger (node_architecture_types_engine_dynamics.timestampedTrigger input);
                                            packet' = let
                                                        target' = whoAsked;
                                                        mailbox'0 = Some 0;
                                                        message' = MsgTicker Count
                                                      in (| MessagePacket.target = target', MessagePacket.mailbox = mailbox'0, MessagePacket.message = message' |)
                                          in (| EnvelopedMessage.sender = sender', EnvelopedMessage.packet = packet' |)];
                     timers' = [];
                     spawnedEngines' = []
                   in (| ActionEffect.newEnv = newEnv', ActionEffect.producedMessages = producedMessages', ActionEffect.timers = timers', ActionEffect.spawnedEngines = spawnedEngines' |) |
                 v \<Rightarrow>
                   let
                     newEnv' = env';
                     producedMessages' = [];
                     timers' = [];
                     spawnedEngines' = []
                   in (| ActionEffect.newEnv = newEnv', ActionEffect.producedMessages = producedMessages', ActionEffect.timers = timers', ActionEffect.spawnedEngines = spawnedEngines' |)))"

fun tickerConflictSolver :: "TickerMatchableArgument AVLTree \<Rightarrow> (TickerMatchableArgument AVLTree) list" where
  "tickerConflictSolver v = []"



end
