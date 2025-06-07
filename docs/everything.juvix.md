---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - index
  - juvix
---


# Everything

```juvix
module everything;
```

## Prelude

```juvix
import prelude;
```

## System

```juvix
import arch.system.identity.identity;
```

### Resource Machine

```juvix
import arch.system.state.resource_machine.data_structures.transaction.transaction_with_payment;
import arch.system.state.resource_machine.data_structures.transaction.transaction;
import arch.system.state.resource_machine.data_structures.transaction.transaction_function;
import arch.system.state.resource_machine.data_structures.transaction.delta_proof;
import arch.system.state.resource_machine.data_structures.compliance_unit.compliance_proof;
import arch.system.state.resource_machine.data_structures.compliance_unit.compliance_unit;
import arch.system.state.resource_machine.data_structures.action.resource_logic_proof;
import arch.system.state.resource_machine.data_structures.action.index;
import arch.system.state.resource_machine.data_structures.resource.computable_components.resource_commitment;
import arch.system.state.resource_machine.data_structures.resource.computable_components.kind;
import arch.system.state.resource_machine.data_structures.resource.computable_components.nullifier;
import arch.system.state.resource_machine.data_structures.resource.computable_components.delta;
import arch.system.state.resource_machine.data_structures.resource.computable_components.introduction;
import arch.system.state.resource_machine.data_structures.resource.index;
import arch.system.state.resource_machine.primitive_interfaces.transaction_function_vm;
import arch.system.state.resource_machine.primitive_interfaces.set;
import arch.system.state.resource_machine.primitive_interfaces.nullifier_set;
import arch.system.state.resource_machine.primitive_interfaces.map;
import arch.system.state.resource_machine.primitive_interfaces.proving_system.proving_system_types;
import arch.system.state.resource_machine.primitive_interfaces.proving_system.proving_system_delta;
import arch.system.state.resource_machine.primitive_interfaces.fixed_size_type.fixed_size_type;
import arch.system.state.resource_machine.primitive_interfaces.fixed_size_type.hash;
import arch.system.state.resource_machine.primitive_interfaces.fixed_size_type.delta_hash;
import arch.system.state.resource_machine.primitive_interfaces.fixed_size_type.arithmetic;
import arch.system.state.resource_machine.primitive_interfaces.index;
import arch.system.state.resource_machine.primitive_interfaces.ordered_set;
import arch.system.state.resource_machine.primitive_interfaces.commitment_accumulator;
import arch.system.state.resource_machine.notes.storage;
import arch.system.state.resource_machine.notes.function_formats.transaction_function_format;
import arch.system.state.resource_machine.notes.applications;
import arch.system.state.resource_machine.notes.roles_and_requirements;
import arch.system.state.resource_machine.notes.nockma;
import arch.system.state.resource_machine.notes.nockma_runnable;
import arch.system.state.resource_machine.notes.runnable;
import arch.system.state.resource_machine.index;
import arch.system.state.resource_machine.execution_flow.flow;
```
