---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

## Create

Given a set of components required to produce a transaction, the create function produces a transaction data structure, which involves computing the nullifiers of the consumed resources, commitments of the created resources, transaction $\Delta$, and all the required proofs.

Assuming that the produced transaction induces a state change consuming resources $r_{i_1},\cdots, r_{i_n}$ and creating resources $r_{o_1}, \cdots, r_{o_m}$, the inputs and outputs of the create function are defined as follows.

Input: 

- a set of $CMtree$ roots $\{rt_{i_k}, k \leq n\}$
- a set of resources $\{r_{i_1},...,r_{i_n}, r_{o_1},...,r_{o_m}\}$
- a set of nullifier secret keys $\{nk_{i_1},...,nk_{i_n}\}$
- extra data $app\_data$
- preference function $\Phi$
- custom inputs required for resource logic proofs

Output: a transaction $tx = (rts cms, nfs, \Pi, \Delta_{tx}, app\_data, \Phi)$, where:

- $rts= \{rt_{i_1},..,rt_{i_n}\}$
- $nfs = \{nf_{i_k} = h_{nf}(nk_{i_l}, r_{i_l}), k = 1..n\}$
- $cms = \{cm_{o_1} = h_{cm}(r_{o_l}), k = 1..m\}$
- $\Pi = \{\pi_{\Delta_{tx}}, \pi_{compl_1}, ..., \pi_{compl_c}, \pi_{i_1}, ..., \pi_{i_n}, \pi_{o_1}, ...,\pi_{o_m}\}$, where $1 \leq c \leq m + n$
- $\Delta_{tx} = \sum_k{\Delta_{i_k}} - \sum_l{\Delta_{o_l}}$
- $app\_data$
- $\Phi$

## Compose

Taking two transactions $tx_1$ and $tx_2$ as input, produces a new transaction $tx = tx_1 \circ tx_2$ according to the [transaction composition rules](./../transaction.md#composition).

## Verify

Taking a transaction as input, verifies its validity according to the [transaction validity rules](./../transaction.md#validity). If the transaction is valid, the resource machine outputs a state update. Otherwise, the output is empty.