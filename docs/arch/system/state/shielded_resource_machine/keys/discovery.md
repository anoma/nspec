# Simple discovery mechanism

The simple discovery mechanism is used to allow for faster discovery of the resources. In the future it might be replaced by our SSS design. The general idea is that the sender encrypts a string that identifies the intended receiver using the receiver's discovery key.

Users can give their discovery keys to computationally powerful parties such as indexers to delegate the discovery process. In that case, indexers will be able to see what transactions are sent to what users (only for the users who gave the keys to them). They will not have access to the transaction payload.

In principle, discovery mechanism is vulnerable to the same issue as the verifiable encryption mechanism and should be verified, but we do not verify discovery payload for efficiency. The only consequence of a malicious action would be that the intended receiver will receive the message later (after the full discovery process discovers the message).

The algorithm for discovery encryption is exactly the same as for payload encryption. We use DH to derive the keys and AES256-GCM to encrypt the payload.
