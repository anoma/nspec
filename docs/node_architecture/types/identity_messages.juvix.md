---
icon: octicons/container-24
search:
  exclude: false
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.types.identity_messages;

    import prelude open;
    import node_architecture.types.identity_types open;
    import node_architecture.basics open;
    ```




DecryptRequest & DecryptResponse

```juvix
type DecryptRequest := mkDecryptRequest {
  data : ByteString;
};

type DecryptResponse := mkDecryptResponse {
  data : ByteString;
  error : Maybe String;
};
```

EncryptRequest & EncryptResponse

```juvix
type EncryptRequest := mkEncryptRequest {
  data : ByteString;
  externalIdentity : ExternalIdentity;
  useReadsFor : Bool;
};

type EncryptResponse := mkEncryptResponse {
  ciphertext : ByteString;
  error : Maybe String;
};
```

CommitRequest & CommitResponse

```juvix
type CommitRequest := mkCommitRequest {
  data : Signable;
};

type CommitResponse := mkCommitResponse {
  commitment : Commitment;
  error : Maybe String;
};
```

VerifyRequest & VerifyResponse

```juvix
type VerifyRequest := mkVerifyRequest {
  commitment : Commitment;
  data : ByteString;
  externalIdentity : ExternalIdentity;
  useSignsFor : Bool;
};

type VerifyResponse := mkVerifyResponse {
  result : Bool;
};
```

ReadsForRequest & ReadsForResponse

```juvix
type ReadsForRequest := mkReadsForRequest {
  externalIdentityA : ExternalIdentity;
  externalIdentityB : ExternalIdentity;
};

type ReadsForResponse := mkReadsForResponse {
  readsFor : Bool;
};
```

SubmitReadsForEvidenceRequest & SubmitReadsForEvidenceResponse

```juvix
type SubmitReadsForEvidenceRequest := mkSubmitReadsForEvidenceRequest {
  evidence : ReadsForEvidence;
};

type SubmitReadsForEvidenceResponse := mkSubmitReadsForEvidenceResponse {
  error : Maybe String;
};
```

QueryReadsForEvidenceRequest & QueryReadsForEvidenceResponse

```juvix
type QueryReadsForEvidenceRequest := mkQueryReadsForEvidenceRequest {
  externalIdentity : ExternalIdentity;
};

type QueryReadsForEvidenceResponse := mkQueryReadsForEvidenceResponse {
  evidence : Set ReadsForEvidence;
};
```

SignsForRequest & SignsForResponse

```juvix
type SignsForRequest := mkSignsForRequest {
  externalIdentityA : ExternalIdentity;
  externalIdentityB : ExternalIdentity;
};

type SignsForResponse := mkSignsForResponse {
  signsFor : Bool;
};
```

SubmitSignsForEvidenceRequest & SubmitSignsForEvidenceResponse

```juvix
type SubmitSignsForEvidenceRequest := mkSubmitSignsForEvidenceRequest {
  evidence : SignsForEvidence;
};

type SubmitSignsForEvidenceResponse := mkSubmitSignsForEvidenceResponse {
  error : Maybe String;
};
```

QuerySignsForEvidenceRequest & QuerySignsForEvidenceResponse

```juvix
type QuerySignsForEvidenceRequest := mkQuerySignsForEvidenceRequest {
  externalIdentity : ExternalIdentity;
};

type QuerySignsForEvidenceResponse := mkQuerySignsForEvidenceResponse {
  evidence : Set SignsForEvidence;
};
```

ResolveNameRequest & ResolveNameResponse

```juvix
type ResolveNameRequest := mkResolveNameRequest {
  name : IdentityName;
};

type ResolveNameResponse := mkResolveNameResponse {
  identities : Set ExternalIdentity;
};
```

SubmitNameEvidenceRequest & SubmitNameEvidenceResponse

```juvix
type SubmitNameEvidenceRequest := mkSubmitNameEvidenceRequest {
  evidence : IdentityNameEvidence;
};

type SubmitNameEvidenceResponse := mkSubmitNameEvidenceResponse {
  error : Maybe String;
};
```

QueryNameEvidenceRequest & QueryNameEvidenceResponse

```juvix
type QueryNameEvidenceRequest := mkQueryNameEvidenceRequest {
  externalIdentity : ExternalIdentity;
};

type QueryNameEvidenceResponse := mkQueryNameEvidenceResponse {
  evidence : Set (Pair IdentityName IdentityNameEvidence);
};
```