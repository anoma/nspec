---
icon: octicons/code-16
search:
  exclude: false
---

# Finalize Auction on deadline elapsed {V2 Template Example}

Typical direct causes are

- the timer of the auction deadline elapsing.

## Auction deadline elapsed

The deadline is elapsed if the auctioneer has received
a [[DeadlineElapsed|deadline elapsed]] message from 
the clock that was tracking this timer.
(There is always at most one such timer set per auctioneer engine.)

## Finalize auction

The auctioneer is settling the second-prize auction.

### State update

Discard all data, except for KYC data.

### Messages to be sent

- Send messages to all bidders.
- Notify winner with payment instructions.

### Engines to be spawned

None

### timers to be set

None




