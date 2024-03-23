# Tokens

*Tokens* are transferrable units of accounting.

The resource logic of tokens enforces two properties:
- *Supply conservation* (implicitly) - in any transaction, tokens must be conserved. This is enforced using the balance check.
- *Ownership* - any transaction which consumes tokens owned by resource `R` must be authorized by `R`. This is checked by requiring the presence of a message from `R` that authorises the consumption of tokens subject to an arbitrary predicate being satisfied in the partial transaction in which the tokens are consumed.
- *Minting* - tokens may reference a particular resource `R` which is allowed to mint new tokens of the denomination (ex nihilo).

Tokens can include arbitrary properties (as data), which may be meaningful to other applications. Properties in static data affect fungibility (determine different tokens), while properties in dynamic data do not (and, absent other restrictions, can be altered by the transaction creator, so could be used for some kind of memo).

*Fungible* tokens are those with a supply of more than 1, while *non-fungible* tokens have a supply of only 1 (such that there is only 1 valid copy in existence at any point in logical time).