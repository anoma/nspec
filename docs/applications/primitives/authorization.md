# Authorization

Authorisation is performed by user-defined resource logics. Users can send a message by creating a resource that can only be created by a valid partial transaction including their account resource and the creation of the message resource. Typically, users will use stateful authorisation (carried by a non-fungible token, essentially) which they can upgrade over time.

- *Stateful* user accounts are identified by a resource, which can be consumed and recreated, and may include dynamic data (such that e.g. users could change keys or authorisation logic over time).
- *Stateless* user accounts are identified by a fixed predicate, which cannot change its logic. This can be useful where users want to prove to an application or third party that they cannot change their logic in some way.
