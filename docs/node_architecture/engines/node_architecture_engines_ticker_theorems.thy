theory node_architecture_engines_ticker_theorems
imports Main
        prelude
        node_architecture_engines_ticker
begin

theorem TickerNeverDecrements: "counter (localState (env x)) \<le> counter (localState (newEnv (action TickerEngineFamily x)))"
proof (cases x)
  case (fields guardOutput env timestampedTrigger)
  then have xdef: "x =  \<lparr>ActionInput.guardOutput = guardOutput, env = env, timestampedTrigger = timestampedTrigger\<rparr>"
    by auto
  then show ?thesis 
    proof (cases guardOutput)
      case (fields args label other)
      then have gdef: "guardOutput = \<lparr>GuardOutput.args = args, label = label, other = other\<rparr>"
        by auto
      then show ?thesis 
        proof (cases label)
          case DoIncrement
          then show ?thesis 
            apply (simp add: TickerEngineFamily_def xdef gdef)
            by (metis (mono_tags, lifting) EngineEnvironment.simps(8) Suc_n_not_le_n counter.simps le_eq_less_or_eq linorder_not_le localState.elims localState.simps)
        next
          case DoRespond
          then have ldef: "label = DoRespond"
            by auto
          then show ?thesis 
          proof (cases args)
            case Nil
            then show ?thesis
              by (simp add: TickerEngineFamily_def xdef gdef ldef)
          next
            case (Cons a list)
            then have ardef: "args = Cons a list"
              by auto
            then show ?thesis 
            proof (cases a)
              case (ReplyTo x1 x2)
              then have adef: "a = ReplyTo x1 x2"
                by auto
              then show ?thesis 
              proof (cases x1)
                case None
                then show ?thesis 
                  by (simp add: TickerEngineFamily_def xdef gdef ldef ardef adef)
              next
                case (Some a)
                then show ?thesis 
                  by (simp add: TickerEngineFamily_def xdef gdef ldef ardef adef)
              qed
            qed
          qed
        qed
    qed
qed

end
