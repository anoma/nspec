---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Naming Engine

The naming engine is responsible for tracking naming information as described in
[[Identity#identity-names|Identity Names]]. It supports name resolution,
submitting name evidence, and querying name evidence. Ultimately, this means
that the Naming Engine tracks which [[IdentityName]]s correspond with which
[[ExternalIdentity]]s using [[IdentityNameEvidence]].

## Messages

- [ResolveNameRequestResponse](./resolve_name_request_response.md)
- [SubmitNameEvidenceRequestResponse](./submit_name_evidence_request_response.md)
- [QueryNameEvidenceRequestResponse](./query_name_evidence_request_response.md)
