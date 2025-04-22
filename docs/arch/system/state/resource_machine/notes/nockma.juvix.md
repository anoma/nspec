---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.state.resource_machine.notes.nockma;
    import prelude open;
    import Stdlib.Data.Nat open;
    import Stdlib.Data.List open;
    ```

# Nockma Implementation

```juvix
-- Operation codes for Nockma:
-- 0: Slash (/)
-- 1: Constant: Returns operand unchanged
-- 2: Apply/Ap/S:
-- 3: Cell test (?): Tests if noun is cell
-- 4: Increment (+): Add 1 to atom
-- 5: Equality test (=): Compare nouns
-- 6: If-then-else
-- 7: Compose
-- 8: Extend subject
-- 9: Invoke (call function by arm name)
-- 10: Pound (#)
-- 11: Match: Case split on Cells vs Atoms
-- 12: Scry (read storage)

-- Basic Nock types
type Noun :=
  | Atom : Nat -> Noun
  | Cell : Noun -> Noun -> Noun;

terminating
nounEq (n1 n2 : Noun) : Bool :=
  case mkPair n1 n2 of {
    | mkPair (Noun.Atom x) (Noun.Atom y) := x == y
    | mkPair (Noun.Cell a b) (Noun.Cell c d) := nounEq a c && nounEq b d
    | _ := false
  };

instance EqNoun : Eq Noun := Eq.mk@{ isEqual := nounEq };

-- Helper to convert storage values to Nouns
axiom convertToNoun : {val : Type} -> val -> Noun;
-- Helper to convert Nouns to storage values
axiom convertFromNoun : {val : Type} -> Noun -> Option val;

type ScryOp :=
  | Direct
  | Index;

type Storage addr val := mkStorage {
  readDirect : addr -> Option val;
  readIndex : val -> Option val
};

axiom externalStorage : {addr val : Type} -> Storage addr val;

type NockOp :=
  | Slash -- /
  | Constant -- Returns operand unchanged
  | Apply
  | CellTest -- ?
  | Increment -- +
  | EqualOp -- =
  | IfThenElse -- 6
  | Compose -- 7
  | Extend -- 8
  | Invoke -- 9
  | Pound -- #
  | Match -- 11
  | Scry; -- 12

opOr {A : Type} (n m : Option A) : Option A :=
  case n of {
    | none := m
    | (some n) := some n
  };

parseOp (n : Nat) : Option NockOp :=
  let test := \{m op :=
    case (n == m) of {
      | true := some op
      | false := none
    }} in
  foldr opOr none
    (zipWith test
      [0; 1; 2; 3; 4; 5; 6; 7; 8; 9; 10; 11; 12]
      [NockOp.Slash; NockOp.Constant; NockOp.Apply; NockOp.CellTest; NockOp.Increment;
      NockOp.EqualOp; NockOp.IfThenElse; NockOp.Compose; NockOp.Extend; NockOp.Invoke;
      NockOp.Pound; NockOp.Match; NockOp.Scry]);

-- Monad to encompass gas consumption and error handling.
type GasState A := mk {
  runGasState : Nat -> Result String (Pair A Nat)
};

instance
GasStateMonad : Monad GasState := Monad.mk@{
  applicative := Applicative.mk@{
    functor := Functor.mk@{
      map := \{f s := GasState.mk \{gas :=
        case GasState.runGasState s gas of {
          | ok (mkPair x remaining) := ok (mkPair (f x) remaining)
          | error e := error e
        }}
    }};
    pure := \{x := GasState.mk \{gas := ok (mkPair x gas)}};
    ap := \{sf sa := GasState.mk \{gas :=
      case GasState.runGasState sf gas of {
        | ok (mkPair f remaining) :=
          case GasState.runGasState sa remaining of {
            | ok (mkPair x final) := ok (mkPair (f x) final)
            | error e := error e
          }
        | error e := error e
      }}
    }
  };
  bind := \{ma f := GasState.mk \{gas :=
    case GasState.runGasState ma gas of {
      | ok (mkPair a remaining) := GasState.runGasState (f a) remaining
      | error e := error e
    }}
  }
};

err {A : Type} (str : String) : GasState A := GasState.mk \{_ := error str};

-- Gas cost values for each operation type
-- These are made up for demo purposes
getGasCost (cost : NockOp) : Nat :=
  case cost of {
    | NockOp.Slash := 1
    | NockOp.CellTest := 1
    | NockOp.Increment := 1
    | NockOp.EqualOp := 2
    | NockOp.IfThenElse := 3
    | NockOp.Compose := 2
    | NockOp.Extend := 2
    | NockOp.Invoke := 3
    | NockOp.Pound := 1
    | NockOp.Scry := 10
    | _ := 0
  };

consume (op : NockOp) : GasState Unit :=
  GasState.mk \{gas :=
  let cost := getGasCost op in
  case cost > gas of {
    | true := error "Out of gas"
    | false := ok (mkPair unit (sub gas cost))
  }};

-- Implementation of storage read operations (scrying)
scry {val : Type} (stor : Storage Nat val) (op : ScryOp) (addr : Nat) : Result String Noun :=
  case op of {
    | ScryOp.Direct := case Storage.readDirect stor addr of {
      | some val := ok (convertToNoun val)
      | none := error "Direct storage read failed"
    }
    | ScryOp.Index := case Storage.readDirect stor addr of {
      | some indexFn := case Storage.readIndex stor indexFn of {
        | some val := ok (convertToNoun val)
        | none := error "Index computation failed"
      }
      | none := error "Index function not found"
    }
  };

-- Helper for slash (/) operations
terminating
slash {val : Type} (stor : Storage Nat val) (n : Noun) (subject : Noun) : GasState Noun :=
  case n of {
    | Noun.Atom x := case x == 1 of {
      | true := pure subject -- Rule: /[1 a] -> a
      | false := case x == 2 of {
        | true := case subject of { -- Rule: /[2 a b] -> a
          | Noun.Cell a _ := pure a
          | _ := err "Cannot take slash of atom"
        }
        | false := case x == 3 of {
          | true := case subject of { -- Rule: /[3 a b] -> b
            | Noun.Cell _ b := pure b
            | _ := err "Cannot take slash of atom"
          }
          | false := case (mod x 2) == 0 of {
            | true :=  -- Rule: /[(a + a) b] -> /[2 /[a b]]
                consume NockOp.Slash >>= \{_ :=
                slash stor (Noun.Atom (div x 2)) subject >>= \{res :=
                consume NockOp.Slash >>= \{_ :=
                slash stor (Noun.Atom 2) res
                }}}
            | false := -- Rule: /[(a + a + 1) b] -> /[3 /[a b]]
                consume NockOp.Slash >>= \{_ :=
                slash stor (Noun.Atom (div x 2)) subject >>= \{res :=
                consume NockOp.Slash >>= \{_ :=
                slash stor (Noun.Atom 3) res
                }}}
          }
        }
      }
    }
    | _ := err "Slash must be atom"
  };

-- Helper for pound (#) operations
terminating
pound {val : Type} (stor : Storage Nat val) (n : Noun) (b : Noun) (c : Noun) : GasState Noun :=
  case n of {
    | Noun.Atom x := case x == 1 of {
      | true := pure b  -- Rule: #[1 a b] -> a
      | false := case mod x 2 == 0 of {
        | true := case c of { -- Rule: #[(a + a) b c] -> #[a [b /[(a + a + 1) c]] c]
          | Noun.Cell _ _ :=
            consume NockOp.Slash >>= \{_ :=
            slash stor (Noun.Atom ((2 * div x 2) + 1)) c >>= \{slashResult :=
            consume NockOp.Pound >>= \{_ :=
            pound stor (Noun.Atom (div x 2)) (Noun.Cell b slashResult) c
            }}}
          | _ := err "Invalid pound target"
        }
        | false := case c of { -- Rule: #[(a + a + 1) b c] -> #[a [/[(a + a) c] b] c]
          | Noun.Cell _ _ :=
            consume NockOp.Slash >>= \{_ :=
            slash stor (Noun.Atom (2 * div x 2)) c >>= \{slashResult :=
            consume NockOp.Pound >>= \{_ :=
            pound stor (Noun.Atom (div x 2)) (Noun.Cell slashResult b) c
            }}}
          | _ := err "Invalid pound target"
        }
      }
    }
    | _ := err "Pound must be atom"
  };

terminating
evalOp {val : Type} (stor : Storage Nat val) (op : NockOp) (a : Noun) (args : Noun) : GasState Noun :=
  case op of {
    -- *[a 0 b] -> /[b a]
    | NockOp.Slash := slash stor args a

    -- *[a 1 b] -> b
    | NockOp.Constant := pure args

    -- *[a 2 b c] -> *[*[a b] *[a c]]
    | NockOp.Apply := case args of {
      | Noun.Cell b c :=
        nock stor (Noun.Cell a b) >>= \{r1 :=
        nock stor (Noun.Cell a c) >>= \{r2 :=
        nock stor (Noun.Cell r1 r2)
        }}
      | _ := err "Invalid apply args"
    }

    -- *[a 3 b] -> ?*[a b]
    -- ?[a b] -> 0
    -- ?a -> 1
    | NockOp.CellTest := case args of {
      | Noun.Cell b _ :=
        nock stor (Noun.Cell a b) >>= \{res :=
        case res of {
          | Noun.Cell _ _ := pure (Noun.Atom 0)
          | _ := pure (Noun.Atom 1)
        }
        }
      | _ := err "Invalid cell test args"
    }

    -- *[a 4 b] -> +*[a b]
    -- +[a b] -> +[a b]
    -- +a -> 1 + a
    | NockOp.Increment := case args of {
      | Noun.Cell b _ :=
        nock stor (Noun.Cell a b) >>= \{res :=
        case res of {
          | (Noun.Atom n) := pure (Noun.Atom (suc n))
          | x := pure x  -- +[a b] -> +[a b] case
        }
        }
      | _ := err "Invalid increment args"
    }

    -- *[a 5 b c] -> =*[a b] *[a c]
    -- =[a a] -> 0
    -- =[a b] -> 1
    | NockOp.EqualOp := case args of {
      | Noun.Cell b c :=
        nock stor (Noun.Cell a b) >>= \{r1 :=
        nock stor (Noun.Cell a c) >>= \{r2 :=
        pure (Noun.Atom (case nounEq r1 r2 of {
              | true := 0
              | false := 1
            }))
        }}
      | _ := err "Invalid equality args"
    }

    -- *[a 6 b c d] -> *[a *[[c d] 0 *[[2 3] 0 *[a 4 4 b]]]]
    | NockOp.IfThenElse := case args of {
      | Noun.Cell b (Noun.Cell c d) :=
        nock stor (Noun.Cell a (Noun.Cell (Noun.Atom 4) (Noun.Cell (Noun.Atom 4) b))) >>= \{r1 :=
        nock stor (Noun.Cell (Noun.Cell (Noun.Atom 2) (Noun.Atom 3)) (Noun.Cell (Noun.Atom 0) r1)) >>= \{r2 :=
        nock stor (Noun.Cell (Noun.Cell c d) (Noun.Cell (Noun.Atom 0) r2)) >>= \{r3 :=
        nock stor (Noun.Cell a r3)
        }}}
      | _ := err "Invalid if-then-else args"
    }

    -- *[a 7 b c] -> *[*[a b] c]
    | NockOp.Compose := case args of {
      | Noun.Cell b c :=
        nock stor (Noun.Cell a b) >>= \{r :=
        nock stor (Noun.Cell r c)
        }
      | _ := err "Invalid compose args"
    }

    -- *[a 8 b c] -> *[[*[a b] a] c]
    | NockOp.Extend := case args of {
      | Noun.Cell b c :=
        nock stor (Noun.Cell a b) >>= \{r :=
        nock stor (Noun.Cell (Noun.Cell r a) c)
        }
      | _ := err "Invalid extend args"
    }

    -- *[a 9 b c] -> *[*[a c] 2 [0 1] 0 b]
    | NockOp.Invoke := case args of {
      | Noun.Cell b c :=
        nock stor (Noun.Cell a c) >>= \{core :=
        let formula := Noun.Cell (Noun.Atom 2) (Noun.Cell (Noun.Cell (Noun.Atom 0) (Noun.Atom 1)) (Noun.Cell (Noun.Atom 0) b)) in
        nock stor (Noun.Cell core formula)
        }
      | _ := err "Invalid invoke args"
    }

    -- *[a 10 [b c] d] -> #[b *[a c] *[a d]]
    | NockOp.Pound := case args of {
      | Noun.Cell (Noun.Cell b c) d :=
        nock stor (Noun.Cell a c) >>= \{r1 :=
        nock stor (Noun.Cell a d) >>= \{r2 :=
        pound stor b r1 r2
        }}
      | _ := err "Invalid pound args"
    }

    -- *[a 11 [b c] d] -> *[[*[a c] *[a d]] 0 3]
    -- *[a 11 b c] -> *[a c]
    | NockOp.Match := case args of {
      | Noun.Cell (Noun.Cell b c) d :=
        nock stor (Noun.Cell a c) >>= \{r1 :=
        nock stor (Noun.Cell a d) >>= \{r2 :=
        nock stor (Noun.Cell (Noun.Cell r1 r2) (Noun.Cell (Noun.Atom 0) (Noun.Atom 3)))
        }}
      | Noun.Cell _ c := nock stor (Noun.Cell a c)
      | _ := err "Invalid pure pound args"
    }

    -- *[a 12 b c d] -> result <- SCRY b c; *[a result d]
    | NockOp.Scry := case args of {
      | Noun.Cell b (Noun.Cell c d) :=
          -- First evaluate b to get the opcode
          nock stor b >>= \{opcode :=
            case opcode of {
              | Noun.Atom opval :=
                  -- Then evaluate c to get the address
                  nock stor c >>= \{addr :=
                    case addr of {
                      | Noun.Atom addrVal :=
                          -- Convert opcode to ScryOp
                          let scryType := case opval == 0 of {
                            | true := ScryOp.Direct
                            | false := ScryOp.Index
                          } in
                          -- Perform the scry operation and wrap result in GasState
                          GasState.mk \{gas :=
                            scry stor scryType addrVal >>= \{scryResult :=
                            -- Continue evaluation with the scry result
                            GasState.runGasState (nock stor (Noun.Cell a (Noun.Cell scryResult d))) gas
                            }
                          }
                      | _ := err "Scry address must be atom"
                    }
                  }
              | _ := err "Scry type must be atom"
            }
          }
      | _ := err "Invalid scry args"
    }
  };

-- Core Nockma evaluator
terminating
nock {val : Type} (stor : Storage Nat val) (input : Noun) : GasState Noun :=
  case input of {
    -- Rule: *a -> *a
    | Noun.Atom _ := pure input

    | Noun.Cell a b := case b of {

      | Noun.Cell first rest := case first of {
        -- Rule: *[a [b c] d] -> [*[a b c] *[a d]]
        | Noun.Cell b c :=
          nock stor (Noun.Cell a (Noun.Cell b c)) >>= \{r1 :=
          nock stor (Noun.Cell a rest) >>= \{r2 :=
          pure (Noun.Cell r1 r2)
          }}

        | Noun.Atom n := case parseOp n of {
          | some opcode := consume opcode >>= \{_ :=
              evalOp stor opcode a rest
            }
          | none := err "Invalid operation"
        }
      }
      | _ := err "Invalid Nock expression"
    }
  };
```
