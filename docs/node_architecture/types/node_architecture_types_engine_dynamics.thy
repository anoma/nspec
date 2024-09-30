theory node_architecture_types_engine_dynamics
imports Main
        node_architecture_basics
        node_architecture_types_anoma_message
        node_architecture_types_engine_environment
        node_architecture_types_anoma_environment
begin

record ('A, 'L, 'X) GuardOutput =
  args :: "'A list"
  label :: 'L
  other :: 'X

fun args :: "('A, 'L, 'X) GuardOutput \<Rightarrow> 'A list" where
  "args (| GuardOutput.args = args', GuardOutput.label = label', GuardOutput.other = other' |) =
    args'"

fun label :: "('A, 'L, 'X) GuardOutput \<Rightarrow> 'L" where
  "label (| GuardOutput.args = args', GuardOutput.label = label', GuardOutput.other = other' |) =
    label'"

fun other :: "('A, 'L, 'X) GuardOutput \<Rightarrow> 'X" where
  "other (| GuardOutput.args = args', GuardOutput.label = label', GuardOutput.other = other' |) =
    other'"

type_synonym ('I, 'H, 'S, 'M, 'A, 'L, 'X) Guard = 
  "('I, 'H) TimestampedTrigger \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> (('A, 'L, 'X) GuardOutput) option"

(* TODO: remove this when the compiler is fixed *)
record ('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput =
  guardOutput :: "('A, 'L, 'X) GuardOutput"
  env :: "('S, 'I, 'M, 'H) EngineEnvironment"
  timestampedTrigger :: "('I, 'H) TimestampedTrigger"

(* TODO: do we need this? *)
record ('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect =
  newEnv :: "('S, 'I, 'M, 'H) EngineEnvironment"
  producedMessages :: "(node_architecture_types_anoma_message.Msg EnvelopedMessage) list"
  timers :: "('H Timer) list"
  spawnedEngines :: "node_architecture_types_anoma_environment.Env list"

fun guardOutput :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput \<Rightarrow> ('A, 'L, 'X) GuardOutput" where
  "guardOutput (| ActionInput.guardOutput = guardOutput', ActionInput.env = env', ActionInput.timestampedTrigger = timestampedTrigger' |) =
    guardOutput'"

fun env :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment" where
  "env (| ActionInput.guardOutput = guardOutput', ActionInput.env = env', ActionInput.timestampedTrigger = timestampedTrigger' |) =
    env'"

fun timestampedTrigger :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput \<Rightarrow> ('I, 'H) TimestampedTrigger" where
  "timestampedTrigger (| ActionInput.guardOutput = guardOutput', ActionInput.env = env', ActionInput.timestampedTrigger = timestampedTrigger' |) =
    timestampedTrigger'"

fun newEnv :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment" where
  "newEnv (| ActionEffect.newEnv = newEnv', ActionEffect.producedMessages = producedMessages', ActionEffect.timers = timers', ActionEffect.spawnedEngines = spawnedEngines' |) =
    newEnv'"

fun producedMessages :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect \<Rightarrow> (node_architecture_types_anoma_message.Msg EnvelopedMessage) list" where
  "producedMessages (| ActionEffect.newEnv = newEnv', ActionEffect.producedMessages = producedMessages', ActionEffect.timers = timers', ActionEffect.spawnedEngines = spawnedEngines' |) =
    producedMessages'"

fun timers :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect \<Rightarrow> ('H Timer) list" where
  "timers (| ActionEffect.newEnv = newEnv', ActionEffect.producedMessages = producedMessages', ActionEffect.timers = timers', ActionEffect.spawnedEngines = spawnedEngines' |) =
    timers'"

fun spawnedEngines :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect \<Rightarrow> node_architecture_types_anoma_environment.Env list" where
  "spawnedEngines (| ActionEffect.newEnv = newEnv', ActionEffect.producedMessages = producedMessages', ActionEffect.timers = timers', ActionEffect.spawnedEngines = spawnedEngines' |) =
    spawnedEngines'"

end
