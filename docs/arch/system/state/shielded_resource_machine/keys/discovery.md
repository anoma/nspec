# Resource discovery

Resources that are distributed in-band have to be discovered by the receiver. The simplest way to do that is to trial decrypt every transaction, which can be computationally expensive for the user. The user can delegate this task to a more computationally powerful entity, which makes it more efficient, but less secure for the user. One way to improve the security properties of delegated discovery is to introduce a discovery plaintext that can be used to discover transactions without decrypting the resource plaintext.

### Simple discovery

A simple discovery mechanism duplicates the resource encryption mechanism but encrypts a fixed string. The discovery server knows that a message is sent to the user if the decrypted message is equal to the expected string.

### Discovery mechanism

Each potential receiver has a static discovery key pair. To enable faster discovery for the message, the sender:

1. generates an ephemeral discovery key pair $(edsk, edpk)$
2. using the receiver's static discovery public key, generates the discovery encryption key $dek = KDF(DH(sdpk_{R}, edsk_{S}), edpk_{S})$
3. encrypts a fixed string `ds` $cd = Encrypt(dek, ds)$ and includes the discovery message in the transaction payload: `discoveryPayload = [cd, edpk_{S}]`

#### Discovery

Given the relevant key $sdsk$ by the potential receiver, the discovery server tries to decrypt each discovery message for each published transaction:

1. using an ephemeral key attached to the payload, they generate the discovery encryption key $dek = KDF(DH(sdsk_{R}, edpk_{S}), edpk{S})$
2. they decrypt a discovery string $ds = Decrypt(dek, cd)$
3. if `ds` is equal to the expected value, the transaction is sent to the user. The user can decrypt the resource payload to get the resource sent to them.

#### Resource decryption

To decrypt a resource, the user:

1. using an ephemeral key attached to the payload, they generate the resource encryption key $rek = KDF(DH(sesk_{R}, eepk_{S}), eepk{S})$
2. they decrypt the resource object $resource = Decrypt(rek, ce)$


#### Verifiable discovery

In principle, discovery mechanism is vulnerable to the same issue as the verifiable encryption mechanism and should be verified, but we do not verify discovery payload for efficiency. The only consequence of a malicious action would be that the intended receiver will receive the message later (after the full discovery process discovers the message).

### Instantiations

Same as for resource encryption.

|Function|Instantiation|
|-|-|
|Encryption algorithm|AES256-GCM|
|KDF|SHA256|
