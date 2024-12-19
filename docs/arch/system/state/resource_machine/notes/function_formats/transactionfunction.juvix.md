```juvix
module arch.system.state.resource_machine.notes.function_formats.transactionfunction;
import prelude open;
```

```juvix
trait
type TransactionFunction (prog addr val gas idx tx : Type) :=
  mkTransactionFunction@{
    readStorage : addr -> prog;
    readByIndex : prog -> prog;
    cost : prog -> gas;
  };

trait
type TransactionVM (prog addr val gas idx tx : Type) :=
  mkTransactionVM@{
    {{txFunc}} : TransactionFunction prog addr val gas idx tx;
    eval : prog -> gas -> Result String tx;
  };
```
