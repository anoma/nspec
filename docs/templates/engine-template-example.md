# Auctioneer 

## Purpose 

The Auctioneer is taking bids and announces the winner.
The auctioneer is responsible for a single auction.

## Auctioneer-specific types

### Bool${}^2$: the local engine specific state

Keep track of wether the auction is started
and whether the deadline has passed.

### Bid

A bid is a pair of an external id and an integer amount.


## [paradigmatic message sequence diagram] (optional)


```mermaid
sequenceDiagram
    participant Bidder1
    participant Bidder2
    participant Auctioneer
    participant Clock
```


## _All_ "Conversation Partners" (Engine _types_)

### Conversation Diagram (optional)


```mermaid
erDiagram
  Auctioneer ||--o{ Bid : receive
  Bid ||--|| Bidder : sent
```

### Bidder

The bidder will send bids and wait for announcement of the winner.

## Guarded Actions

### Receive Bid

<details>
  <summary>Consider a bid from a bidder.</summary>
  <p>That's it (in this example).</p>
</details> 

### Finalize Auction
<details>
  <summary>After deadline has passed, the winner is announced.</summary>
  <p>That's it.</p>
</details> 
