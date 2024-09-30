theory node_architecture_types_engine_family
imports Main
        node_architecture_basics
        node_architecture_types_anoma_message
        node_architecture_types_engine_environment
        node_architecture_types_engine_dynamics
begin

record ('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily =
  guards :: "(('I, 'H) TimestampedTrigger \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> (('A, 'L, 'X) GuardOutput) option) list"
  action :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionInput \<Rightarrow> ('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionEffect"
  conflictSolver :: "'A AVLTree \<Rightarrow> ('A AVLTree) list"

record ('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine =
  name :: "(string, nat) Either"
  family :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily"
  initEnv :: "('S, 'I, 'M, 'H) EngineEnvironment"

fun guards :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily \<Rightarrow> (('S, 'I, 'M, 'H, 'A, 'L, 'X) Guard) list" where
  "guards (| EngineFamily.guards = guards', EngineFamily.action = action', EngineFamily.conflictSolver = conflictSolver' |) =
    guards'"

fun action :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily \<Rightarrow> ('S, 'I, 'M, 'H, 'A, 'L, 'X) ActionFunction" where
  "action (| EngineFamily.guards = guards', EngineFamily.action = action', EngineFamily.conflictSolver = conflictSolver' |) =
    action'"

fun conflictSolver :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily \<Rightarrow> 'A AVLTree \<Rightarrow> ('A AVLTree) list" where
  "conflictSolver (| EngineFamily.guards = guards', EngineFamily.action = action', EngineFamily.conflictSolver = conflictSolver' |) =
    conflictSolver'"

fun name :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine \<Rightarrow> Name" where
  "name (| Engine.name = name', Engine.family = family', Engine.initEnv = initEnv' |) = name'"

fun family :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine \<Rightarrow> ('S, 'I, 'M, 'H, 'A, 'L, 'X) EngineFamily" where
  "family (| Engine.name = name', Engine.family = family', Engine.initEnv = initEnv' |) = family'"

fun initEnv :: "('S, 'I, 'M, 'H, 'A, 'L, 'X) Engine \<Rightarrow> ('S, 'I, 'M, 'H) EngineEnvironment" where
  "initEnv (| Engine.name = name', Engine.family = family', Engine.initEnv = initEnv' |) = initEnv'"

end
