# Finalize Auction when deadline elapses {V2 Template Example}

Typical direct causes are

- the timer of the auction deadline elapsing.

## Auction deadline elapsed

The deadline is elapsed if the auctioneer has received
a [[DeadlineElapsed|deadline elapsed]] message from 
the clock that was tracking this timer.
(There is always at most one such timer set per auctioneer engine.)

## Finalize auction

The auctioneer is settling the second-prize auction.

### state update

Discard all data, except for KYC data.

### messages to be sent

- Broadcast winning bid to all participants.
- Notify winner with payment instrucions.

### engines to be spawned

N/A

### timers to be set

N/A




