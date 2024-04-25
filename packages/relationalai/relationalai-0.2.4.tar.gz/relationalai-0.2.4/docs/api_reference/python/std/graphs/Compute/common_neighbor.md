# `relationalai.std.graphs.Compute.common_neighbor()`

```python 
relationalai.std.graphs.Compute.common_neighbor(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that computes the
the common neighbors between the producers passed to `node1` and `node2`. 

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

Returns an [Expression](docs/api_reference/python/Expression.md) that produces object ID of the common node.

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

# Compute the common neighbor between each pair of distinct people.
with model.query() as select:
    person1 = Person()
    person2 = Person()
    person1 != person2
    person2 != person1
    common_neighbor= graph.compute.common_neighbor(person1, person2)
    response = select(person1.name, person2.name, common_neighbor.name)

print(response.results)
# Output:
#      name  name2  name3
# 0   Alice    Bob  Carol
# 1   Alice  Carol    Bob
# 2   Alice   Dave    Bob
# 3   Alice   Dave  Carol
# 4     Bob  Alice  Carol
# 5     Bob  Carol  Alice
# 6     Bob  Carol   Dave
# 7     Bob   Dave  Carol
# 8   Carol  Alice    Bob
# 9   Carol    Bob  Alice
# 10  Carol    Bob   Dave
# 11  Carol   Dave    Bob
# 12   Dave  Alice    Bob
# 13   Dave  Alice  Carol
# 14   Dave    Bob  Carol
# 15   Dave  Carol    Bob
```
