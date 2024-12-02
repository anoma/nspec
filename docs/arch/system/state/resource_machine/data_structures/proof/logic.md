# Resource Logic

A resource logic is a computable predicate associated with a resource that constrains the creation and consumption of a resource. Each time a resource is attempted to be created or consumed, the corresponding resource logic proof is required to approve the action.

Every proof has three types of inputs and constraints:

1. *Architecture-level* inputs and constraints. This type of inputs and constraints allow to enforce certain resource machine properties and have to be present in each resource logic, no matter in the context of which instantiation and application the resource logic was produced. These contraints ensure basic resource machine properties.
2. *Instantiation-level* inputs and constraints. These inputs and constraints must be present in every resource logic compatible with a concrete resource machine instantiation but might not be required by other instantiations. These constraints ensure additional resource machine properties desired by the instantiation.
3. *Application-level* (custom) inputs and constraints that are present in every resource logic specified by a concrete application. These constraints define how the application works.

This specification explicitly defines only the architecture-level inputs and constraints. Only application-level constraints are referred to as custom.

## Proving

When proving, resource logics take as input resources created and consumed in the action:

#### Instance

1. [`tag`](./../resource/computable_components/tag.md) — identifies the current resource being checked
2. `action.consumed` (possibly excluding the tagged resource, if it is consumed)
3. `action.created` (possibly excluding the tagged resource, if it is created)
4. `action.applicationData`

#### Witness

1. for consumed resources:
    1. resource object
    2. `nullifierKey`
2. for created resources:
    1. resource object
3. Application inputs

!!! note
    The instance and witness values are expected to correspond to each other: the first tag in the instance corresponds to the first resource object in the witness (and corresponds to the resource being checked), and so on. Note that the tag has to be recomputed from the object to verify that it indeed corresponds to the tag (this condition is included in the constraints)

#### Constraints

1. Created commitment integrity: `r.commitment() = cm`
2. Consumed nullifier integrity: `r.nullifier(nullifierKey) = nf`
3. Application constraints