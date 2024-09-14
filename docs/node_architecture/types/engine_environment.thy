theory engine_environment
imports Main
        basics
        anoma_message
begin

record ('S, 'I, 'M, 'H) EngineEnvironment =
  name :: "(string, nat) Either"
  (* read-only *)
  localState :: 'S
  mailboxCluster :: "(nat, ('I, 'M) Mailbox) Map"
  acquaintances :: "((string, nat) Either) Set"
  timers :: "('H Timer) list"

fun name :: "('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> Name" where
  "name (| EngineEnvironment.name = name', EngineEnvironment.localState = localState', EngineEnvironment.mailboxCluster = mailboxCluster', EngineEnvironment.acquaintances = acquaintances', EngineEnvironment.timers = timers' |) =
    name'"

fun localState :: "('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> 'S" where
  "localState (| EngineEnvironment.name = name', EngineEnvironment.localState = localState', EngineEnvironment.mailboxCluster = mailboxCluster', EngineEnvironment.acquaintances = acquaintances', EngineEnvironment.timers = timers' |) =
    localState'"

fun mailboxCluster :: "('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> (nat, ('I, 'M) Mailbox) Map" where
  "mailboxCluster (| EngineEnvironment.name = name', EngineEnvironment.localState = localState', EngineEnvironment.mailboxCluster = mailboxCluster', EngineEnvironment.acquaintances = acquaintances', EngineEnvironment.timers = timers' |) =
    mailboxCluster'"

fun acquaintances :: "('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> Name Set" where
  "acquaintances (| EngineEnvironment.name = name', EngineEnvironment.localState = localState', EngineEnvironment.mailboxCluster = mailboxCluster', EngineEnvironment.acquaintances = acquaintances', EngineEnvironment.timers = timers' |) =
    acquaintances'"

fun timers :: "('S, 'I, 'M, 'H) EngineEnvironment \<Rightarrow> ('H Timer) list" where
  "timers (| EngineEnvironment.name = name', EngineEnvironment.localState = localState', EngineEnvironment.mailboxCluster = mailboxCluster', EngineEnvironment.acquaintances = acquaintances', EngineEnvironment.timers = timers' |) =
    timers'"

end
