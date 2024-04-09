# Kudos


- fungible assets ~ cryptographic kudos
	- issuance
	- point-in-time payments (multihop)
	- rpgf
		- pay-to-identity
		- pay-to-denomination
	- rebalancing (mutual credit issuance)


causal model of events
theory of value
want to reward whatever led to the production of this value

## Cryptographic kudos


_Cryptographic kudos_ are a transferable resource class. They come in fungible and non-fungible varieties with arbitrary properties and are always associated with an initial issuing identity. In general, cryptographic kudos are _transferable_ - this is what makes them "kudos" instead of just directed or undirected relationships in those DAGs, and this is why linearity is important - although they may have specific restrictions on when or how tranfers can be performed in specific cases.

## Issuance


Kudos cam be issued with a signature from the identity of their initial controller. Different denominations of kudos could possibly limit the rate of issuance with respect to a known external clock, but in general limitations on rate of issuance are not assumed for many of the systemic properties of interest.

## Transfer


Kudos can be transferred with a signature from their latest (rightmost) controller.

## Liquidity provisioning


Kudo liquidity can be provisioned using appropriate intents (partial transactions).

## Routing


Routes can be found for possible chained kudo exchanges in a privacy-preserving way by consulting the associated issuing identities.

## Pay-to-holders


Payment can be made to the holders of a particular kudo denomination at a particular point in logical time, who then can claim it pro-rata later.

## Pay-to-holders-integral


Payment can be made to the holders of a particular kudo denomination over time (integral), who then can claim it fraction-by-time pro-rata later.

!!! todo

     Here, we might need a human-time shared clock, since that's kinda what we want to model.
