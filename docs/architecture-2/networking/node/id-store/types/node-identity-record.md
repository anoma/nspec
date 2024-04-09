# NodeIdentityRecord


## Purpose


Record stored about a node identity.

## Type


*Struct* with the following fields.

| Field        | Type                                              | Description                          |
|--------------|---------------------------------------------------|--------------------------------------|
| `id`         | *[[NodeIdentity#nodeidentity]]*                   | Node identity                        |
| `advert`     | *Option\<[[NodeAdvert#nodeadvert]]\>*           | Node advertisement                   |
| `trust`      | *Option\<[[TrustValue#trustvalue]]\>*           | Trust value                          |
| `reputation` | *Option\<[[ReputationValue#reputationvalue]]\>* | Reputation value                     |
| `tprefs`     | *Option\<[[TransportPrefs#transportprefs]]\>*   | Transport preferences for this peer  |
| `cprefs`     | *Option\<[[ConnectionPrefs#connectionprefs]]\>* | Connection preferences for this peer |
