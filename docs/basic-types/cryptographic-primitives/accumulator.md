---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Accumulator

An _accumulator_ must support the following functionality:

- $WRITE(cm)$ adds an element to the accumulator, returning the witness used to prove membership. 
- $WITNESS(cm)$ for a given element, returns the witness used to prove membership if the element is present, otherwise returns nothing.
- $VERIFY(cm, w, acc)$ verifies the membership proof for an element $cm$ with a membership witness $w$ in the accumulator $acc$.
- $ACC()$ returns the accumulator.