theory node_architecture_engines_ticker_theorems
imports Main
        prelude
        node_architecture_engines_ticker
begin

theorem TickerNeverDecrements: "counter (localState (env x)) \<le> counter (localState (newEnv (action TickerEngineFamily x)))"
proof -
  obtain guardOutput env timestampedTrigger args label other where xdef:
    "x = \<lparr>ActionInput.guardOutput = \<lparr>GuardOutput.args = args, label = label, other = other\<rparr>, env = env, timestampedTrigger = timestampedTrigger\<rparr>"
    by (metis ActionInput.cases GuardOutput.cases)
  show ?thesis
  proof (cases label)
    case DoIncrement
    then show ?thesis
      by (simp add: TickerEngineFamily_def xdef)
         (metis EngineEnvironment.simps(8) Suc_n_not_le_n counter.simps le_eq_less_or_eq
                linorder_not_le localState.elims localState.simps)
  next
    case DoRespond
    then have ldef: "label = DoRespond" by auto
    then show ?thesis
    proof (cases args)
      case Nil
      then show ?thesis by (simp add: TickerEngineFamily_def xdef ldef)
    next
      case (Cons a list)
      then have rdef: "args = Cons a list" by auto
      obtain x1 x2 where adef: "a = ReplyTo x1 x2"  by (cases a) auto
      then show ?thesis by (cases x1; simp add: TickerEngineFamily_def xdef ldef rdef adef)
    qed
  qed
qed

end
