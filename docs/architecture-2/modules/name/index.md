---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Naming Engine

The naming engine is responsible for tracking naming information as described in
[Identity Names](../../../architecture-1/abstractions/identity.md#identity-names).
It supports name resolution, submitting name evidence, and querying name
evidence. Ultimately, this means that the Naming Engine tracks which
[[IdentityName]]s correspond with which [[ExternalIdentity]]s using
[[IdentityNameEvidence]].

## Messages

- [ResolveNameRequestResponse](./resolve-name-request-response.md)
- [SubmitNameEvidenceRequestResponse](./submit-name-evidence-request-response.md)
- [QueryNameEvidenceRequestResponse](./query-name-evidence-request-response.md)
