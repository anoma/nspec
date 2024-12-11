---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Kind

For a resource `r`, its kind is computed as: `r.kind() = kindHash(r.labelRef, r.logicRef)`.

<!--ᚦ«where kindHash is a deltahash function »-->
