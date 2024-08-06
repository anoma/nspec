---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Counter application

This example describes the mechanics of counters associated with a specific controller, implemented in a resource model.

## `CounterId` resource (application)

`CounterId` resource represents a counter tied to a specific controller that is used to initialise other counters. In a sense, it can be seen as a counter of counters. `CounterId` resource can be seen as an atomic counter (in a broad sense) application. For that reason, we describe it in the application terms. 

### `CounterId` application interface

- **Init:** creates a new `CounterId` resource with a zero value.
- **Update:** updates an existing `CounterId` resource from value $n$ to value $n + 1$.

### `CounterId` application logic constraints

- The quantity of each `CounterId` resource must be the same, set to a non-zero constant value $q$. 
- Each `CounterId` resource must have the controller's public key in the label. 
- A signature from the controller authorising the transaction must be provided (verified with the key stored in the label).
- Init case: The value (representing the current count) must be set to 0. The transaction must be balanced by a consumed ephemeral resource of the same kind. 
- Update case: The value of the created resource must be set to $n + 1$ where $n$ is the value of the consumed resource of the same kind.

## Counter application

Counter resource represents a simple counter. 

### `Counter` application interface

- **Init:** a new counter is initialised from the current counterId resource (the counterId value goes to the counter resource label). When a new counter is created, the `CounterId` resource is updated to ensure there are no counters that have the same label.
- **Update:** An existing `Counter` resource can be updated from value $n$ to value $n + 1$.

### `Counter` application logic constraints

- The quantity of each counterId resource must be the same, set to a non-zero constant value $q$. 
- Each `Counter` resource must have the controller's public key in the label and a value of the `CounterId` resource from the moment the `Counter` resource was initialised.
- Init case: 
     - The label and the value are set to the value of the `CounterId` resource updated in the same transaction function. The transaction must be balanced by a consumed ephemeral resource of the same kind. 
     - The resource kind of the `CounterId` resource must be verified to ensure that this is indeed the `CounterId` resource's value is used to derive the `Counter` resource label. 
- Update case: 
    - The value of the created resource must be set to $n + 1$ where $n$ is the value of the consumed resource of the same kind.

In this simple version, updating the counter requires no special permissions but the counter resource logic can be modified to be more complex and have more restricted counter update rules.

<figure markdown="span">
![image](/docs/images/counter_diagram.svg){ width="450" }
<figcaption markdown="span">
CounterId and Counter applications interfaces
</figcaption>
</figure>