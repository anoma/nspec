theory engine_family
imports Main
        basics
        anoma_message
        engine_environment
        engine_dynamics
begin

record ('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily =
  guards :: "(nat option \<Rightarrow> ('I, 'H) Trigger \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> (('A, 'L, 'X) GuardOutput) option) Set"
  action :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput \<Rightarrow> (('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect) option"
  conflictSolver :: "'A Set \<Rightarrow> ('A Set) list"

record ('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine =
  name :: "(string, nat) Either"
  family :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily"
  initEnv :: "('S, 'I, 'M, 'H) EngineEnvironment"

fun guards :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily \<Rightarrow> (nat option \<Rightarrow> ('I, 'H) Trigger \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> (('A, 'L, 'X) GuardOutput) option) Set" where
  "guards (| EngineFamily.guards = guards', EngineFamily.action = action', EngineFamily.conflictSolver = conflictSolver' |) =
    guards'"

fun action :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily \<Rightarrow> ('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput \<Rightarrow> (('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect) option" where
  "action (| EngineFamily.guards = guards', EngineFamily.action = action', EngineFamily.conflictSolver = conflictSolver' |) =
    action'"

fun conflictSolver :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily \<Rightarrow> 'A Set \<Rightarrow> ('A Set) list" where
  "conflictSolver (| EngineFamily.guards = guards', EngineFamily.action = action', EngineFamily.conflictSolver = conflictSolver' |) =
    conflictSolver'"

fun name :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine \<Rightarrow> Name" where
  "name (| Engine.name = name', Engine.family = family', Engine.initEnv = initEnv' |) = name'"

fun family :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine \<Rightarrow> ('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily" where
  "family (| Engine.name = name', Engine.family = family', Engine.initEnv = initEnv' |) = family'"

fun initEnv :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment" where
  "initEnv (| Engine.name = name', Engine.family = family', Engine.initEnv = initEnv' |) = initEnv'"

end
