# Resource Logic

A resource logic is a computable predicate associated with a resource that constrains the creation and consumption of a resource. Each time a resource is attempted to be created or consumed, the corresponding resource logic proof is required to approve the action.

Every resource logic has three types of inputs and constraints:

1. *Architecture-level* inputs and constraints. This type of inputs and constraints allow to enforce certain resource machine properties and have to be present in each resource logic, no matter in the context of which instantiation and application the resource logic was produced
2. *Instantiation-level* inputs and constraints. These inputs and constraints must be present in every resource logic compatible with a concrete resource machine instantiation but might not be required by other instantiations
3. *Application-level* (custom) inputs and constraints that are present in every resource logic specified by a concrete application

This specification explicitly defines only the architecture-level inputs and constraints. Only application-level constraints are referred to as custom.

## Proving

When proving, resource logics take as input resources created and consumed in the action:

#### Instance 

1. `action.consumed`
2. `action.created`
3. `tag` — identifies the resource being checked. For created resources, `r.tag() = r.commitment()`, for created - `r.tag() = r.nullifier(nullifierKey)`.
4. `action.applicationData`

#### Witness

1. input resources corresponding to the elements of `consumed`
2. output resource corresponding to the elements of `created`
3. custom inputs

!!! note
    The instance and witness values are expected to correspond to each other: the first tag in the instance corresponds to the first resource object in the witness, and so on. Note that the tag has to be recomputed from the object to verify that it indeed corresponds to the tag (included in the constraints)

#### Constraints

1. for each output resource, check that the corresponding `r.cm` value is derived according to the rules specified by the resource machine instance
2. for each input resource, check that the corresponding `r.nf` value is derived according to the rules specified by the resource machine instantiation
3. custom constraints