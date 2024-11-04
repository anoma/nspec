# Resource Logic

A resource logic is a verifiable predicate associated with a resource that constraints the creation and consumption of a resource. Each time a resource is attempted to be created or consumed, the corresponding resource logic proof is required to approve the action.

Every resource logic has three types of inputs and constraints:

- Architecture-level inputs and constraints. This type of inputs and constraints have to be present in each resource logic, no matter in the context of which instantiation and application the resource logic was produced
- Instantiation-level inputs and constraints. These inputs and constraints must be present in every resource logic compatible with a concrete resource machine instantiation but might not be required by other instantiations
- Application-level (custom) inputs and constraints that are present in every resource logic specified by a concrete application

This specification explicitly defines only the architecture-level inputs and constraints. Only application-level constraints are referred to as custom.

## Proving

When proving, resource logics take as input resources created and consumed in the action:

#### Instance 

- `action.consumed`
- `action.created`
- `tag` — identifies the resource being checked. For created resources, `r.tag() = r.commitment()`, for created - `r.tag() = r.nullifier(nullifierKey)`.
- `action.applicationData`

#### Witness

- input resources corresponding to the elements of `consumed`
- output resource corresponding to the elements of `created`
- custom inputs

#### Constraints

- for each output resource, check that the corresponding `r.cm` value is derived according to the rules specified by the resource machine instance
- for each input resource, check that the corresponding `r.nf` value is derived according to the rules specified by the resource machine instantiation
- custom constraints