# Action

## Action trees

The tags of all resources in the action are organized in an action tree. The root of the tree is passed as a part of an instance to each logic associated with the action, and when a resource object is passed in the witness, we verify inclusion of the corresponding tag in the tree.

The depth of the action tree depends on the number of resources in the action. The tree parameters are the same as for the commitment tree.

## Resource logic constraints

Currently there is no way to enforce the presence of any constraints in a resource logic since resource logics are designed by application developers. The constraints that nevertheless have to be present in resource logics for safety reasons are:

1. Ensuring the correspondence of the instance and witness. Specifically, the corresponsence of resource tags and examined resource objects.
2. If in-band encryption is used, verifying the correctness of the encryption.
3. Verifying the tag existence in the action tree.

Since this cannot be included automatically, users must make sure the applications they use have these checks present.
