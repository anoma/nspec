---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Reads For Engine

The Reads For Engine tracks reads_for relationships between identities as
described in [[Identity#readsfor-relation|ReadsFor Relation]]. It supports
querying which identities read for another identity or can read for it,
submitting evidence that one identity reads for another, and querying evidence
concerning known reads_for relationships.

## Messages

- [[ReadsForRequestResponse]]
- [[SubmitReadsForEvidenceRequestResponse]]
- [[QueryReadsForEvidenceRequestResponse]]
