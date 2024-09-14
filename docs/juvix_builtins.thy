theory juvix_builtins
  imports Main
          "HOL-Library.Finite_Map" 
begin

consts ordNatI :: nat

type_synonym 'a Set = "'a fset"

definition SetfromList :: "'a \<Rightarrow> 'a list \<Rightarrow> 'a Set" where
  "SetfromList _ = FSet.fset_of_list"

type_synonym ('a, 'b) Map = "('a, 'b) fmap"

definition MapfromList :: "'a \<Rightarrow> ('a \<times> 'b) list \<Rightarrow> ('a, 'b) Map" where
  "MapfromList _ = Finite_Map.fmap_of_list"

type_synonym Unit = unit

definition unit :: Unit where
  "unit = ()"

end
