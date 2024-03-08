(* Sometimes it is useful to have a name for an external identity
    before the relevant cryptographic values are available.
ANCHOR: encryptor_name_description
An `identityName` can be mapped to an appropriate `Encryptor.encryptor`
 when suitable `evidence` is found. 
Here, `checkEncryptorName` defines what evidence is acceptable for a
 `Encryptor.encryptor`. 
Note that `identityName`s are also hashable: we require a structure
 `EncryptorNameHash` that details how to hash them. 
 * ANCHOR_END: encryptor_name_description *)
(* ANCHOR: encryptor_name *)
signature ENCRYPTOR_NAME = sig
  structure Encryptor : ENCRYPTOR
  type evidence
  type identityName
  val checkEncryptorName : identityName -> Encryptor.encryptor -> evidence -> bool
  structure EncryptorNameHash : HASH sharing type EncryptorNameHash.hashable = identityName
end
(* ANCHOR_END: encryptor_name *)

