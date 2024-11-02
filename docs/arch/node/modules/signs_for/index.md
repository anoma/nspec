---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Signs For Engine

The Signs For Engine track signs_for relationships between identities as
described in [[Identity#singsfor-relation|SignsForRelation]]. It
supports querying which identities sign for another identity or can be signed
for by it, submitting evidence that one identity signs for another, and querying
evidence concerning known signs_for relationships.

## Messages

- [[SignsForRequestResponse]]
- [[SubmitSignsForEvidenceRequestResponse]]
- [[QuerySignsForEvidenceRequestResponse]]
