module Test where

postulate
    Digest : Set
    hash : {A : Set} -> A -> Digest
    Option : Set -> Set
    Path : Set
    Pair : Set -> Set -> Set
    Bool : Set
    undef : {A : Set} -> A


record Commitment (A : Set) : Set where
    field
        committed : A
        commitment : Digest


record CommitmentTree (A : Set) (Tree : Set -> Set) : Set where
    field
        hashRoot : Tree A -> Digest
        add : A -> Tree A -> Pair (Tree A) Path
        read : Path -> Tree A -> Option (Commitment A)
        verify : Path -> Commitment A -> Tree A -> Bool

data MTree (A B : Set) : Set where
    mkMTreeLeaf : (value : A) -> MTree A B
    mkMTreeNode : (merge : B) -> (left : MTree A B) -> (right : MTree A B) -> MTree A B

CTree : Set -> Set
CTree A = MTree (Commitment A) Digest


thisShouldWork : {A : Set} -> CommitmentTree A CTree
CommitmentTree.hashRoot (thisShouldWork {A}) = treeHash
    where
        treeHash : {A : Set} -> CTree A -> Digest
        treeHash (mkMTreeLeaf
            record { committed = committed ; commitment = commitment }) = commitment
        treeHash (mkMTreeNode merge left right) = merge
CommitmentTree.add (thisShouldWork {A}) = undef
CommitmentTree.read (thisShouldWork {A}) = undef
CommitmentTree.verify (thisShouldWork {A}) = undef

