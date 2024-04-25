# `relationalai.std.graphs.Compute.preferential_attachment()`

```python
relationalai.std.graphs.Compute.preferential_attachment(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that computes the
[the preferential attachment score](https://en.wikipedia.org/wiki/Preferential_attachment) between the producers passed to `node1` and `node2`. The preferential attachment score between two nodes `node1` and `node2` is the number of nodes adjacent to `node1` multiplied by the number of nodes adjacent to `node2`.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes |   |
| Directed | Yes |   |
| Weighted | Yes | Weights are ignored.   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |
| `node2` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |

## Returns

Returns an [Expression](docs/api_reference/python/Expression.md) that produces the number.

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a `friend` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    dave = Person.add(name="Dave")
    alice.set(friend=bob)
    bob.set(friend=carol).set(friend=dave)
    carol.set(friend=dave).set(friend=alice)

# Create a graph and add all `Person` objects to the set of nodes
# and the `Person.friend` property to the set of edges.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friend)

# Compute the preferential attachment score between each pair of distinct people.
with model.query() as select:
    person1 = Person()
    person2 = Person()
    person1 != person2
    preferential_attachment = graph.compute.preferential_attachment(person1, person2)
    response = select(person1.name, person2.name, preferential_attachment)

print(response.results)
# Output:
#      name  name2  v
# 0   Alice    Bob  6
# 1   Alice  Carol  6
# 2   Alice   Dave  4
# 3     Bob  Alice  6
# 4     Bob  Carol  9
# 5     Bob   Dave  6
# 6   Carol  Alice  6
# 7   Carol    Bob  9
# 8   Carol   Dave  6
# 9    Dave  Alice  4
# 10   Dave    Bob  6
# 11   Dave  Carol  6
```