---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Proof-of-stake

- Tokens of a particular denomination can be locked for a configurable period of time in a non-fungible bond
- Bond can be claimed in the future with rewards as indicated (fixed-rate or variable-rate)

- Bond can be soulbound (?)

- Bond carries voting rights (perhaps somewhat proportional to lockup length)

- Bond is associated with a specific validator selection function

    - Owner of the bond may redelegate (or equivalent)

- Bond gains stake-weighted voting power on funding allocation decisions (logistic function)

- Bonds can also be offered by the protocol for locking other assets

    - Incentive alignment mechanism

    - Coupons still pay out in staking asset

- Targeting controller sets interest (targeting lockup profiles of different denominations)

    - Protocol can also buy back bonds

    - Could include bonds of other denominations

    - Pro rata redemption (exit) is allowed, with a controller-determined tax

Additional options

- Non-transferable bonds (requires some kind of anti-collusion anti-transfer mechanism)

- Free gas per unit time for stakers (non-transferable)
