# `relationalai.std.graphs.Compute.weighted_degree_centrality()`

```python
relationalai.std.graphs.Compute.weighted_degree_centrality(node: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that produces the
the weighted degree centrality value for the producer passed to `node`

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--------- | :-------- | :---- |
| Directed   | Yes       |  Edge weights default to `1.0`     |
| Undirected | Yes       |  Edge weights default to `1.0`      |
| Weighted | Yes |   |

## Parameters

| Name   | Type                                      | Description                                   |
| :----- | :---------------------------------------- | :-------------------------------------------- |
| `node` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |

## Returns

An [`Expression`](../../../Expression.md) object that produces `float` values.

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model named "transactions" with a Person and Transaction type.
model = rai.Model("transactions")
Person = model.Type("Person")
Transaction = model.Type("Transaction")

# Add some people and transactions to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    Transaction.add(amount=10, payer=alice, payee=bob)
    Transaction.add(amount=25, payer=alice, payee=carol)
    Transaction.add(amount=1500, payer=bob, payee=carol)
    
# Create a weihted graph that connects people based on the number of transactions 
# with the amount as the weight.
graph = Graph(model, weighted=True)

with model.rule():
    t = Transaction()
    graph.Edge.add(t.payer, t.payee, weight=t.amount)

# Compute the weighted degree centrality of each person in the graph.
with model.query() as select:
    person = Person()
    centrality = graph.compute.weighted_degree_centrality(person)
    response = select(person.name, centrality)

print(response.results)
# Output:
#     name      v
# 0  Alice   17.5
# 1    Bob  755.0
# 2  Carol  762.5
```

## See Also

[`Compute.degree_centrality`](./degree_centrality.md)
