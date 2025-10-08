# Verifiable encryption

Resource objects are encrypted and included in the transaction to enable in-band distribution of resources. Encrypted resources are stored on the blockchain, the receiver can scan the blockchain, trying to decrypt the transactions, to find the resources that were sent to them.

We want the encryption to be _verifiable_ to make sure the receiver of the resources can decrypt them. In systems like Zcash the sender and the creator of the resource are usually the same entity, and it doesn't make sense for the sender to send a corrupted message to the receiver (essentially burning the resource), therefore, no need to verify correctness of the encryption. In our case, the resources are sent by users, but often created by solvers, and we need to make sure that the solvers correctly encrypt the resources.

Not all of the resource-related fields have to be encrypted (e.g. the resource commitment), and the encrypted fields may vary depending on the application. To make sure it is flexible enough, the encryption check is performed in RL circuits (as opposed to verifying the encryption in the compliance circuit).

### Encryption algorithm

Each potential receiver has a static encryption key pair. To send a resource to a user, the sender:

1. generates an ephemeral encryption key pair $(eesk, eepk)$
2. using the receiver's static encrypion public key, generates the resource encryption key $rek = KDF(DH(sepk_{R}, eesk_{S}), eepk_{S})$
3. encrypts the resource $ce = Encrypt(rek_{AB}, r)$ and includes the encrypted message in the transaction payload: `resourcePayload = [ce, eepk_{A}]`

The receiver has to [discover]() the message sent to them and then decrypt it, inverting the process above.

### Instantiations

|Function|Instantiation|
|-|-|
|Encryption algorithm|AES256-GCM|
|KDF|SHA256|
