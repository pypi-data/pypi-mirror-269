# `relationalai.std.graphs.Compute.adamic_adar()`

```python
relationalai.std.graphs.Compute.adamic_adar(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that computes the
[Adamic Adar index](https://en.wikipedia.org/wiki/Adamic%E2%80%93Adar_index)
between the producers passed to `node1` and `node2`.
The Adamic Adar index measures the similarity of two nodes `node1` and `node2` according to the amount of shared edges between them.

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

An [`Expression`](../../../Expression.md) object that produces `float` values.

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

# Compute the Adamic Adar index between each pair of distinct people.
with model.query() as select:
    person1 = Person()
    person2 = Person()
    person1 != person2
    adamic_adar_index = graph.compute.adamic_adar(person1, person2)
    response = select(person1.name, person2.name, adamic_adar_index)

print(response.results)
# Output:
#      name  name2         v
# 0   Alice    Bob  0.910239
# 1   Alice  Carol  0.910239
# 2   Alice   Dave  1.820478
# 3     Bob  Alice  0.910239
# 4     Bob  Carol  2.885390
# 5     Bob   Dave  0.910239
# 6   Carol  Alice  0.910239
# 7   Carol    Bob  2.885390
# 8   Carol   Dave  0.910239
# 9    Dave  Alice  1.820478
# 10   Dave    Bob  0.910239
# 11   Dave  Carol  0.910239
```