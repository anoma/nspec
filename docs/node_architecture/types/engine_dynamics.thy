theory engine_dynamics
  imports Main
    basics
    anoma_message
    engine_environment
    anoma_environment
begin

record ('A, 'L, 'X) GuardOutput =
  args :: "'A list"
  label :: 'L
  other :: 'X

type_synonym ('I, 'H, 'S, 'M, 'A, 'L, 'X) Guard = 
  "('I, 'H) TimestampedTrigger \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> (('A, 'L, 'X) GuardOutput) option"

record ('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput =
  guardOutput :: "('A, 'L, 'X) GuardOutput"
  env :: "('S, 'I, 'M, 'H) EngineEnvironment"
  trigger :: "('I, 'H) TimestampedTrigger"

record ('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect =
  newEnv :: "('S, 'I, 'M, 'H) EngineEnvironment"
  producedMessages :: "(Msg EnvelopedMessage) list"
  timers :: "('H Timer) list"
  spawnedEngines :: "Env list"

end
