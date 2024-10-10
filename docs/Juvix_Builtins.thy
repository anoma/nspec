theory Juvix_Builtins
  imports Main
          "HOL-Library.Finite_Map" 
begin

consts ordNatI :: nat

type_synonym 'a AVLTree = "'a fset"

locale Data_Set_AVL
begin

definition fromList :: "'a \<Rightarrow> 'a list \<Rightarrow> 'a AVLTree" where
  "fromList _ = FSet.fset_of_list"

definition empty :: "'a AVLTree" where
  "empty = fromList undefined []"

end

type_synonym ('a, 'b) Map = "('a, 'b) fmap"


locale Data_Map
begin

definition fromList :: "'a \<Rightarrow> ('a \<times> 'b) list \<Rightarrow> ('a, 'b) Map" where
  "fromList _ = Finite_Map.fmap_of_list"

definition empty :: "('a, 'b) Map" where
  "empty = fmempty"

end

type_synonym Unit = unit

definition unit :: Unit where
  "unit = ()"

type_synonym ('a, 'b) Pair = "'a \<times> 'b"

locale Pair
begin

definition pair :: "'a \<Rightarrow> 'b \<Rightarrow> ('a, 'b) Pair" where
  "pair a b = (a , b)"

end

definition option_bind :: "'a option \<Rightarrow> ('a \<Rightarrow> 'b option) \<Rightarrow> 'b option" where
  "option_bind m f = (
    case m of
      (Some x) \<Rightarrow> (f x) |
      None \<Rightarrow> None
  )"


end
