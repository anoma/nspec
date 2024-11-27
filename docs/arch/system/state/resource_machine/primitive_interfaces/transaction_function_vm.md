# Transaction function VM

Transaction function VM is used to interpret transaction functions. 

## Interface

- `eval(TransactionFunction, GasLimit) -> Transaction`

Examples: 
- nock (transparent-only; transaction function) 
- (?) cairo, risc0 (circuits)

!!! warning
    TODO: are nock and cairo/risc0 on the same level? What exactly transaction functions look like in cairo/risk0 case? What about the relationship with proving systems?
