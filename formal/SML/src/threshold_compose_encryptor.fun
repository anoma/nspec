(* DANGER: NOT YET IMPLEMENTED
 * Implementing this requires secret sharing.
 *
 * The threshold composed `encryptor` is a threshold, and a set of weights
 * paired with `UnderlyingEncryptor.encryptor`s. There are stored in a `Map.map`
 * under their hashes, to ensure uniqueness. 
 *
 * The idea is that an encrypted `plaintext` should only be
 *  decryptable by a `decryptor` that encodes the information from a
 *  set of `decryptor`s corresponding to a set of `encryptor`s whose
 *  weight sums to at least the threshold. 
 *)
functor ThresholdComposeEncryptor (
  structure Encryptor:ENCRYPTOR
  structure Map : ORD_MAP sharing Map.Key = Encryptor.EncryptorHash.OrdKey
  structure ThresholdComposeHash : HASH
    where type hashable = {threshold:int, weights : ((int * Encryptor.encryptor) Map.map)}
  ) : ENCRYPTOR = struct
  structure Map = Map
  structure UnderlyingEncryptor = Encryptor
  structure EncryptorHash = ThresholdComposeHash
  type encryptor = EncryptorHash.hashable
  type plaintext = UnderlyingEncryptor.plaintext
  type ciphertext = UnderlyingEncryptor.ciphertext
  fun compose (threshold : int) (weights : (int * Encryptor.encryptor) list) : encryptor =
    {threshold = threshold,
     weights = foldl (fn ((w,e), m) =>
       Map.insert(m, UnderlyingEncryptor.EncryptorHash.hash e, (w, e))) Map.empty weights}
  fun encrypt _ _ = raise General.Fail "THRESHOLD COMPOSE ENCRYPT IS NOT YET IMPLEMENTED."
end
