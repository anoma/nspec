# Action

## Action trees

The tags of all resources in the action are organized in an action tree. The root of the tree is passed as a part of an instance to each logic associated with the action, and when a resource object is passed in the witness, we verify inclusion of the corresponding tag in the tree.

The depth of the action tree depends on the number of resources in the action. The tree parameters are the same as for the commitment tree.
