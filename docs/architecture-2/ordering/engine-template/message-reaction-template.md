#### `SomeMessageToReactTo`
- _from_ [SendingEngine](#SendingEngine), [AnotherSendingEngine](#AnotherSendingEngine)

##### Purpose
A message typically informs (about "observations" of the sending engine)
or requests data (that the receiving engine is missing).
Thus, it makes sense to make precise, what the purpose of the message is.

##### Structure

| Field           | Type                    | Description                    |
| -----           | ----                    | -----------                    |
| `name_of_field` | [`TypeName`](#TypeLink) | describe the field information |
| ...             | ...                     | ...                            |
| `last_field`    | [`NameN`](#TypeNLink)   | more descriptions              |

##### Effects
- This message may changes the state of the engine instance in certain ways.
- It might impose new obligations ...
- ... resolve obligations.
- …

##### Triggers
- to [Engine](#Engine): [`ReactionMessage`](#ReactionMessage), [`AnotherMessage`](#AnotherMessage)
  `if` \<condition1 one liner\>
  `then` \<message1 contents description\>
  &
  `if` \<condition2 one liner\>
  `then` \<message2 contents description\>
  &
  ...
  &
  `if` \<condition$n$ one liner\>
  `then` \<message$n$ contents description\>

- to [AnotherEngine](#AnotherEngine): [`AnotherReactionMessage`](#AnoterReactionMessage), [`YetAnotherMessage`](#YetAnotherMessage)
  _\[...\]_
- …
