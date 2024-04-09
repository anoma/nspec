# Properties of Anoma instances

## Inclusion fairness

Every transaction candidate submitted by users
to the [[Ordering Machine|ordering machine]]
will eventually be executed (although execution may run into errors).
The user may be required to pay inclusion fees
to accommodate for limited bandwidth or storage.

<!--
☝️ this is for v1 !!!
In v2,
we are going to have some relativized claims
-->

## Time stamping acknowledgments

Every transaction candidate submission may be answered promptly
with a local time stamp of the receiving worker;
however, this is optional.

## Transaction time brackets

Every transaction request is eventually answered by the worker
with a pair of time stamps:
one for the batch opening and one for the batch closing;
the batch opening is the time the receiving worker has started the batch
and
the batch closing is the time when the receiving worker is sending
the corresponding worker hash to its primary.

<!-- in v2, this will be more complicated -->

## Batch ordering consistency

The batches of a worker are ordered such
that it is consistent with the batch time stamps.

## Execution acknowledgment

The user is informed about execution of a transaction candidate
if they wish to be informed.

<!--
## Execution IO

<<The executor engines send themselves the new values of the key-value store.>>
-->

## Reliable Delivery

Every message sent to a cryptographic identity will
eventually be delivered
(if the corresponding engine participates in the peer to peer system).
