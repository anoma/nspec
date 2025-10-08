# Verifiable encryption

Encryption is used for in-band distribution of resources. Encrypted resources are stored on the blockchain, the receiver can scan the blockchain trying to decrypt the transactions to find the resources that were sent to them.

We want the encryption to be verifiable to make sure the receiver of the resources can decrypt them. In other systems like Zcash the sender and the creator of the resource are the same actor, and it doesn't make sense for the sender to send a corrupted message to the receiver (essentially burning the resource), in our case, the resources are sent by users, but often created by solvers.

We derive the encryption keys using DH and encrypt the keys with AES256-GCM.

Not all of the resource-related fields require to be encrypted (e.g. the resource commitment), and the encrypted fields may vary depending on the application. To make sure it is flexible enough, the encryption check is performed in RL circuits (as opposed to verifying the encryption in the compliance circuit).
