# RelationalAI Engine FAQ

## How are concurrent workloads handled by an engine?

Engines are the primary mechanism for performance isolation.
As a general rule, all workloads executing concurrently against the same engine affect each other in some way.
Use separate engines whenever you want to avoid different users having to coordinate their usage.

To illustrate, let's say two developers A and B are working on separate [models](../api_reference/python/Model/README.md),
but both are using the same engine.
Now A loads a large amount of test data.
While the load is ongoing, B will see their model changes spinning.
Then say B introduces an error into their model, unintentionally causing a very expensive, unconstrained computation.
As this happens, A will suddenly experience performance degradation.

## How can I tell if I need more engines?

Use the[RelationalAI CLI](../api_reference/cli/README.md) to check the status of your transactions:

```sh
rai transactions:list
```

If you see transactions sitting in the queued state for any significant amount of time, then the engine has reached its concurrency limit.
Reduce the number of concurrent transactions or redirect some load to an idle engine to free up the engine's CPU.
If you see transactions sitting in the waiting state, then the engine does not have enough memory or IO capacity available to make progress on them.
Cancel the affected transactions and rerun them against an idle engine.
Finally, if transactions sit in the created state, then no engine has been able to even accept them.
This likely means that all available engines are overloaded.

## What are the best practices for creating and using engines?

For large inputs, graph algorithms generally aim to utilize all resources on an engine.
Run at most one large scale graph algorithm per engine at a time.

Each active Snowflake schema requires memory on an engine.
Avoid interacting with more than two or three schemas through a single engine at a time.
Always prefer working with the same engine on the same schema and avoid mixing, as juggling too many active schemas will degrade engine performance.
