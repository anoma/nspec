---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

*Non-linear resource* is a resource that can be consumed multiple times, as opposed to a linear resource, that can only be consumed exactly once. Such resources could be useful to hold external data (e.g., the current gas price) that can be read multiple times. However, having native non-linear resources introduces some challenges as some basic assumptions about resources (e.g., nullifier uniqueness) wouldn't hold any more. At the same time, the resource structure might be unnecessary and excessive for storing such data. For these reasons, **the ARM doesn't support native non-linear resources**.

Without having non-linear resources, such functionality can be achieved from storing the data intended to be read separately and passing it to resource logics as arbitrary input. The authenticity of the provided data has to be verified first, and then it can be used by the resource logic as a valid source of information.