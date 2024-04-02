# Reads For Engine

The Reads For Engine tracks reads-for relationships between identities as described in [ReadsFor Relation](../../architecture-1/abstractions/identity.md#readsfor-relation). It supports querying which identities read for another identity or can read for it, submitting evidence that one identity reads for another, and querying evidence concerning known reads-for relationships.

## Messages

- [ReadsForRequestResponse](./reads-for/reads-for-request-response.md)
- [SubmitReadsForEvidenceRequestResponse](./reads-for/submit-reads-for-evidence-request-response.md)
- [QueryReadsForEvidenceRequestResponse](./reads-for/query-reads-for-evidence-request-response.md)