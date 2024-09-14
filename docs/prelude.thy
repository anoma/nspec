theory prelude
imports Main
        juvix_builtins
begin

definition ten :: nat where
  "ten = 10"

definition verdad :: bool where
  "verdad = True"

definition hello :: string where
  "hello = ''Hello, World!''"

definition unitValue :: Unit where
  "unitValue = unit"

(* necessary for Isabelle-translation *)
definition pair :: "nat \<times> bool" where
  "pair = (42, True)"

datatype ('A, 'B) Either
  = Left 'A |
    Right 'B

definition error :: "(string, nat) Either" where
  "error = Left ''Error!''"

definition answer :: "(string, nat) Either" where
  "answer = Right 42"

definition numbers :: "nat list" where
  "numbers = [1, 2, 3]"

(* alternative syntax: *)
definition niceNumbers :: "nat list" where
  "niceNumbers = [1, 2, 3]"

definition codeToken :: "(nat, string) Map" where
  "codeToken = MapfromList ordNatI [(1, ''BTC''), (2, ''ETH''), (3, ''ANM'')]"

definition uniqueNumbers :: "nat Set" where
  "uniqueNumbers = SetfromList ordNatI [1, 2, 2, 2, 3]"

definition undef :: 'A where
  "undef = undefined"

definition undefinedNat :: nat where
  "undefinedNat = undef Nat"

end
