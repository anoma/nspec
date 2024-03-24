(* HPaxos Message *)

signature HPAXOS_VALUE =
sig
    type t
    val default : t (* default value *)
    val eq : t * t -> bool (* equality *)
end

signature HPAXOS_BALLOT =
sig
    type t
    val zero : t (* the smallest ballot *)
    val eq : t * t -> bool
    val compare : t * t -> order
end

(* --8<-- [start:sml_hpaxos_message] *)
signature HPAXOS_MESSAGE =
sig
    type t
    datatype typ = OneA
                 | OneB
                 | TwoA

    structure Value : HPAXOS_VALUE
    type value = Value.t

    structure Ballot : HPAXOS_BALLOT
    type ballot = Ballot.t

    structure Learner : LEARNER
    type learner = Learner.t

    structure Acceptor : ACCEPTOR
    type acceptor = Acceptor.t

    val hash : t -> word
    val eq : t * t -> bool

    val typ : t -> typ

    val is_one_a : t -> bool
    val is_one_b : t -> bool
    val is_two_a : t -> bool

    val mk_one_b : t option * t list -> t
    val mk_two_a : t option * t list * learner -> t

    (* if the message is 2a, return its learner instance; otherwise, return NONE *)
    val learner : t -> learner option

    (* returns message sender *)
    val sender : t -> acceptor

    (* if the message is 1a, return its ballot and value; otherwise, return NONE *)
    val get_bal_val : t -> (ballot * value) option

    (* returns a previous message of the sender *)
    val get_prev : t -> t option

    (* returns a list of direct references *)
    val get_refs : t -> t list
end
(* --8<-- [end:sml_hpaxos_message] *)

functor MessageOrdKey (Msg : HPAXOS_MESSAGE) : ORD_KEY =
struct
    type ord_key = Msg.t
    fun compare (m1, m2) = Word.compare (Msg.hash m1, Msg.hash m2)
end

functor MessageUtil (Msg : HPAXOS_MESSAGE) =
struct
    structure MsgSet : ORD_SET = RedBlackSetFn (MessageOrdKey (Msg))

    (* fun does_reference_1a m : bool = *)
    (*     isSome (List.find Msg.is_one_a (Msg.get_refs m)) *)

    fun references_exactly_one_1a m : bool =
        let fun check (x, (found, false)) = (found, false)
              | check (x, (false, true)) =
                if Msg.is_one_a x then (true, true) else (false, true)
              | check (x, (true, true)) =
                if Msg.is_one_a x then (true, false) else (true, true)
        in
            case foldl check (false, true) (Msg.get_refs m) of
                (found, no_second) => found andalso no_second
        end

    fun refs_nondup m : bool =
        let
            fun check_unique (_, (refs, false)) = (refs, false)
              | check_unique (x, (refs, true)) =
                if MsgSet.member (refs, x) then
                    (refs, false)
                else
                    (MsgSet.add (refs, x), true)
        in
            #2 (foldl check_unique (MsgSet.empty, true) (Msg.get_refs m))
        end

    (* checks if m2 is in transitive closure of prev for m1 *)
    structure PrevTran :>
              sig
                  val is_prev_reachable : Msg.t * Msg.t -> bool
                  val is_prev_reachable' : (Msg.t -> Msg.Ballot.t) -> Msg.t * Msg.t -> bool
              end =
    struct
    fun is_prev_reachable_aux cont (m1, m2) =
        let fun loop NONE = false
              | loop (SOME m) =
                cont m andalso (Msg.eq (m, m2) orelse loop (Msg.get_prev m))
        in
            loop (SOME m1)
        end

    fun is_prev_reachable (x, y) =
        is_prev_reachable_aux (fn z => true) (x, y)

    fun is_prev_reachable' bal (x, y) =
        let
            val y_bal = bal y
            fun cont z =
                case Msg.Ballot.compare (bal z, y_bal) of
                    LESS => false
                  | _ => true
        in
            is_prev_reachable_aux cont (x, y)
        end
    end (* PrevTran *)

    (* compute transitive references of the message *)
    fun tran pred cont m =
        let
            fun loop accu visited [] = accu
              | loop accu visited (x :: tl) =
                if MsgSet.member (visited, x) then
                    loop accu visited tl
                else
                    let val visited' = MsgSet.add (visited, x) in
                        if cont x then
                            let
                                val accu' = if pred x then x :: accu else accu
                                val queue' = (Msg.get_refs x) @ tl
                            in
                                loop accu' visited' queue'
                            end
                        else
                            loop accu visited' tl
                    end
        in
            loop [] MsgSet.empty [m]
        end
end
