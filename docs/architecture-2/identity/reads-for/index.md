---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Reads For Engine

The Reads For Engine tracks reads-for relationships between identities as described in [ReadsFor Relation](../../../architecture-1/abstractions/identity.md#readsfor-relation). It supports querying which identities read for another identity or can read for it, submitting evidence that one identity reads for another, and querying evidence concerning known reads-for relationships.

## Messages

- [ReadsForRequestResponse](./reads-for-request-response.md)
- [SubmitReadsForEvidenceRequestResponse](./submit-reads-for-evidence-request-response.md)
- [QueryReadsForEvidenceRequestResponse](./query-reads-for-evidence-request-response.md)
