---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

## Post- and pre-ordering execution

*Pre-ordering execution* implies partial evaluation of the transaction function. In practice pre-ordering execution happens before the transactions are ordered by the ordering component external to the ARM.

*Post-ordering execution* implies full evaluation of the transaction function. As the name suggests, post-ordering execution happens after the ordering component external to the ARM completed the ordering of transaction functions.

## ARMs as intent machines

Together with $(CMtree, NFset)$, the Anoma Resource Machine forms an instantiation of the intent machine, where the state $S = (CMtree, NFset)$, a batch $B = Transaction$, and the transaction verification function of the resource machine corresponds to the state transition function of the [intent machine](). To formally satisfy the intent machine's signature, the resource machine's verify function may return the processed transaction along with the new state.


