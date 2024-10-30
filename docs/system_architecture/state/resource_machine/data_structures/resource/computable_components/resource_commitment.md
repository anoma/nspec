---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Commitment

Information flow control property implies working with flexible privacy requirements, varying from transparent contexts, where almost everything is publicly known, to contexts with stronger privacy guarantees, where as little information as possible is revealed.

From the resource model perspective, stronger privacy guarantees require operating on resources that are not publicly known in a publicly verifiable way. Therefore, proving the resource's existence has to be done without revealing the resource's plaintext.

One way to achieve this would be to publish a **commitment** to the resource plaintext. For a resource $r$, the resource commitment is computed as $r.cm = h_{cm}(r)$. Resource commitment has binding and hiding properties, meaning that the commitment is tied to the created resource but does not reveal information about the resource beyond the fact of creation. From the moment the resource is created, and until the moment it is consumed, the resource is a part of the system's state.

>
> The resource commitment is also used as the resource's address $r.addr$ in the content-addressed storage.
> Consumption of the resource does not necessarily affect the resource's status in the storage (e.g., it doesn't get deleted).

