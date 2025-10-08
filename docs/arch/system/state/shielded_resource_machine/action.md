# Action

#### Action trees

All resource tags in the action are organized in an action tree. The root of the tree is passed as an instance, and when a resource object is passed in the witness, we verify inclusion of the corresponding tag in the tree.

The size of the action tree depends on the number of resources in the action. In the witness, it is enough to pass only the relevant to the transaction resource objects.
