```juvix
module Nockma;
import prelude open;
import Stdlib.Data.Nat open;
import Stdlib.Data.List open;
import arch.system.state.resource_machine.notes.function_formats.transactionfunction open;
```

Nockma Implementation:

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

type ScryOp :=
  | Direct
  | Index;

type Storage addr val := mkStorage {
  readDirect : addr -> Option val;
  readIndex : val -> Option val
};

axiom externalStorage : {addr val : Type} -> Storage addr val;

-- Helper to convert storage values to Nouns 
axiom convertToNoun : {val : Type} -> val -> Noun;
-- Helper to convert Nouns to storage values 
axiom convertFromNoun : {val : Type} -> Noun -> Option val;

-- Helper function for checking noun equality
terminating
nounEq (n1 n2 : Noun) : Bool :=
  case mkPair n1 n2 of {
    | mkPair (Atom x) (Atom y) := x == y
    | mkPair (Cell a b) (Cell c d) := nounEq a c && nounEq b d
    | _ := false
  };

instance EqNoun : Eq Noun := mkEq@{ eq := nounEq };

-- Implementation of storage read operations (scrying)
scry {val : Type} (stor : Storage Nat val) (op : ScryOp) (addr : Nat) : Result String Noun :=
  case op of {
    | Direct := case Storage.readDirect stor addr of {
      | some val := ok (convertToNoun val)
      | none := error "Direct storage read failed"
    }
    | Index := case Storage.readDirect stor addr of {
      | some indexFn := case Storage.readIndex stor indexFn of {
        | some val := ok (convertToNoun val)
        | none := error "Index computation failed"
      }
      | none := error "Index function not found"
    }
  };

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

-- Gas cost values for each operation type
-- These are made up for demo purposes
getGasCost (cost : NockOp) : Nat :=
  case cost of {
    | Slash := 1
    | CellTest := 1 
    | Increment := 1
    | EqualOp := 2
    | IfThenElse := 3 
    | Compose := 2
    | Extend := 2
    | Invoke := 3
    | Pound := 1
    | Scry := 10
    | _ := 0
  };

-- Helper function for gas consumption
consume (op : NockOp) (gas : Nat) (cont : Nat -> Result String Noun) : Result String Noun :=
  let gasCost := getGasCost op in
  case gasCost > gas of {
    | true := error "Out of gas"
    | false := cont (sub gas gasCost)
  };

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
      [Slash; Constant; Apply; CellTest; Increment;
      EqualOp; IfThenElse; Compose; Extend; Invoke;
      Pound; Match; Scry]);

-- Helper for slash (/) operations
terminating
slash {val : Type} (stor : Storage Nat val) (gas : Nat) (n : Noun) (subject : Noun) : Result String Noun := 
  case n of {
    | Atom x := case x == 1 of {
      | true := ok subject -- Rule: /[1 a] -> a
      | false := case x == 2 of {
        | true := case subject of { -- Rule: /[2 a b] -> a
          | Cell a _ := ok a
          | _ := error "Cannot take slash of atom"
        }
        | false := case x == 3 of {
          | true := case subject of { -- Rule: /[3 a b] -> b
            | Cell _ b := ok b
            | _ := error "Cannot take slash of atom"
          }
          | false := case (mod x 2) == 0 of {
            | true :=  -- Rule: /[(a + a) b] -> /[2 /[a b]]
                consume Slash gas \{gas :=
                slash stor gas (Atom (div x 2)) subject >>= \{res :=
                consume Slash gas \{gas :=
                slash stor gas (Atom 2) res
                }}}
            | false := -- Rule: /[(a + a + 1) b] -> /[3 /[a b]]
                consume Slash gas \{gas :=
                slash stor gas (Atom (div x 2)) subject >>= \{res :=
                consume Slash gas \{gas :=
                slash stor gas (Atom 3) res
                }}}
          }
        }
      }
    }
    | _ := error "Slash must be atom"
  };

-- Helper for pound (#) operations
terminating
pound {val : Type} (stor : Storage Nat val) (gas : Nat) (n : Noun) (b : Noun) (c : Noun) : Result String Noun := 
  case n of {
    | Atom x := case x == 1 of {
      | true := ok b  -- Rule: #[1 a b] -> a
      | false := case mod x 2 == 0 of {
        | true := case c of { -- Rule: #[(a + a) b c] -> #[a [b /[(a + a + 1) c]] c]
          | Cell _ _ := 
            consume Slash gas \{gas :=
            slash stor gas (Atom ((2 * div x 2) + 1)) c >>= \{slashResult :=
            consume Pound gas \{gas :=
            pound stor gas (Atom (div x 2)) (Cell b slashResult) c
            }}}
          | _ := error "Invalid pound target"
        }
        | false := case c of { -- Rule: #[(a + a + 1) b c] -> #[a [/[(a + a) c] b] c]
          | Cell _ _ := 
            consume Slash gas \{gas :=
            slash stor gas (Atom (2 * div x 2)) c >>= \{slashResult :=
            consume Pound gas \{gas :=
            pound stor gas (Atom (div x 2)) (Cell slashResult b) c
            }}}
          | _ := error "Invalid pound target"
        }
      }
    }
    | _ := error "Pound must be atom"
  };

terminating
evalOp {val : Type} (stor : Storage Nat val) (gas : Nat) (op : NockOp) (a : Noun) (args : Noun) : Result String Noun :=
  case op of {
    -- *[a 0 b] -> /[b a]
    | Slash := slash stor gas args a
    
    -- *[a 1 b] -> b
    | Constant := ok args

    -- *[a 2 b c] -> *[*[a b] *[a c]]
    | Apply := case args of {
      | Cell b c := 
        nock stor gas (Cell a b) >>= \{r1 :=
        nock stor gas (Cell a c) >>= \{r2 :=
        nock stor gas (Cell r1 r2)
        }}
      | _ := error "Invalid apply args"
    }
    
    -- *[a 3 b] -> ?*[a b]
    -- ?[a b] -> 0
    -- ?a -> 1
    | CellTest := case args of {
      | Cell b _ := 
        nock stor gas (Cell a b) >>= \{res :=
        case res of {
          | Cell _ _ := ok (Atom 0)
          | _ := ok (Atom 1)
        }
        }
      | _ := error "Invalid cell test args"
    }

    -- *[a 4 b] -> +*[a b]
    -- +[a b] -> +[a b]
    -- +a -> 1 + a
    | Increment := case args of {
      | Cell b _ := 
        nock stor gas (Cell a b) >>= \{res :=
        case res of {
          | (Atom n) := ok (Atom (suc n))
          | x := ok x  -- +[a b] -> +[a b] case
        }
        }
      | _ := error "Invalid increment args"
    }

    -- *[a 5 b c] -> =*[a b] *[a c]
    -- =[a a] -> 0
    -- =[a b] -> 1 
    | EqualOp := case args of {
      | Cell b c :=
        nock stor gas (Cell a b) >>= \{r1 :=
        nock stor gas (Cell a c) >>= \{r2 :=
        ok (Atom (case nounEq r1 r2 of {
              | true := 0
              | false := 1
            }))
        }}
      | _ := error "Invalid equality args"
    }

    -- *[a 6 b c d] -> *[a *[[c d] 0 *[[2 3] 0 *[a 4 4 b]]]]
    | IfThenElse := case args of {
      | Cell b (Cell c d) :=
        nock stor gas (Cell a (Cell (Atom 4) (Cell (Atom 4) b))) >>= \{r1 :=
        nock stor gas (Cell (Cell (Atom 2) (Atom 3)) (Cell (Atom 0) r1)) >>= \{r2 :=
        nock stor gas (Cell (Cell c d) (Cell (Atom 0) r2)) >>= \{r3 :=
        nock stor gas (Cell a r3)
        }}}
      | _ := error "Invalid if-then-else args"
    }

    -- *[a 7 b c] -> *[*[a b] c]
    | Compose := case args of {
      | Cell b c := 
        nock stor gas (Cell a b) >>= \{r :=
        nock stor gas (Cell r c)
        }
      | _ := error "Invalid compose args"
    }

    -- *[a 8 b c] -> *[[*[a b] a] c]
    | Extend := case args of {
      | Cell b c := 
        nock stor gas (Cell a b) >>= \{r :=
        nock stor gas (Cell (Cell r a) c)
        }
      | _ := error "Invalid extend args"
    }

    -- *[a 9 b c] -> *[*[a c] 2 [0 1] 0 b]
    | Invoke := case args of {
      | Cell b c :=
        nock stor gas (Cell a c) >>= \{core :=
        let formula := Cell (Atom 2) (Cell (Cell (Atom 0) (Atom 1)) (Cell (Atom 0) b)) in
        nock stor gas (Cell core formula)
        }
      | _ := error "Invalid invoke args"
    }

    -- *[a 10 [b c] d] -> #[b *[a c] *[a d]]
    | Pound := case args of {
      | Cell (Cell b c) d := 
        nock stor gas (Cell a c) >>= \{r1 :=
        nock stor gas (Cell a d) >>= \{r2 :=
        pound stor gas b r1 r2
        }}
      | _ := error "Invalid pound args"
    }

    -- *[a 11 [b c] d] -> *[[*[a c] *[a d]] 0 3]
    -- *[a 11 b c] -> *[a c]
    | Match := case args of {
      | Cell (Cell b c) d := 
        nock stor gas (Cell a c) >>= \{r1 :=
        nock stor gas (Cell a d) >>= \{r2 :=
        nock stor gas (Cell (Cell r1 r2) (Cell (Atom 0) (Atom 3)))
        }}
      | Cell _ c := nock stor gas (Cell a c)
      | _ := error "Invalid pure pound args"
    }

    -- *[a 12 b c d] -> result <- SCRY b c; *[a result d]
    | Scry := case args of {
      | Cell b (Cell c d) := 
        case nock stor gas b of {
          | ok (Atom opcode) := 
            case nock stor gas c of {
              | ok (Atom addr) := 
                scry stor (case opcode == 0 of {
                  | true := Direct
                  | false := Index
                }) addr
                >>= \{result := nock stor gas (Cell a (Cell result d))}
              | ok _ := error "Scry address must be atom"
              | err := err
            }
          | ok _ := error "Scry type must be atom"
          | err := err
        }
      | _ := error "Invalid scry args"
    }
  };

-- Core Nockma evaluator 
terminating
nock {val : Type} (stor : Storage Nat val) (gas : Nat) (input : Noun) : Result String Noun := 
  case input of {
    -- Rule: *a -> *a
    | Atom _ := ok input
    
    | Cell a b := case b of {

      | Cell first rest := case first of {
        -- Rule: *[a [b c] d] -> [*[a b c] *[a d]]
        | Cell b c := 
          nock stor gas (Cell a (Cell b c)) >>= \{r1 :=
          nock stor gas (Cell a rest) >>= \{r2 :=
          ok (Cell r1 r2)
          }}

        | Atom n := case parseOp n of {
          | some opcode := consume opcode gas (\{gas' := 
              evalOp stor gas' opcode a rest
            })
          | none := error "Invalid operation"
        }
      }
      | _ := error "Invalid Nock expression"
    }
  };
```

Nockma instances for transaction function functionality;

```juvix
instance
NockmaTransactionFunction : TransactionFunction Noun Nat (Option Noun) Nat Noun Noun :=
  mkTransactionFunction@{
    readStorage := \{addr :=
      Cell (Atom 12) (Cell (Atom 0) (Cell (Atom addr) (Atom 1)))
    };
    readByIndex := \{prog :=
      Cell (Atom 12) (Cell (Atom 1) (Cell prog (Atom 1)))
    };
    cost := \{prog := 
      -- Simple cost model: sums gas cost of all appearing operations
      let
        terminating
        countNodes (n : Noun) : Nat :=
          case n of {
            | Atom a := 
              case parseOp a of {
                | some op := getGasCost op
                | none := 0
              }
            | Cell a b := countNodes a + countNodes b
          };
      in countNodes prog
    };
  };

instance
NockmaVM : TransactionVM Noun Nat (Option Noun) Nat Noun Noun :=
  mkTransactionVM@{
    txFunc := NockmaTransactionFunction;
    eval := \{prog gas := 
      case nock (externalStorage {Nat} {Nat}) gas prog of {
        | ok result := ok result
        | error msg := error msg
      }
    };
  };
```