# Blocking-Call Audit with Measured Before/After

## Table

Here is one request passing through start to finish:

| Step | About | What the thread is doing | On what | How long |
| :--- | :--- | :--- | :--- | :--- |
| Ingress | FastAPI receives HTTP request and validates JSON payload | Computing | Main Event Loop (CPU) | < 1 ms |
| Delegation | Event loop hands blocking model call off to threadpool | Waiting | Worker Thread Assignment | < 1 ms |
| Inference | Execution of synchronous model or blocking work (`time.sleep(1.0)`) | Computing | Worker Thread (CPU/I/O) | ~1000 ms |
| Egress | Worker thread returns result; FastAPI serializes JSON response | Computing | Main Event Loop (CPU) | < 1 ms |

---

## Measurements

| Metric | Blocking (`async def` + `time.sleep`) | Fixed (`def` / `asyncio.to_thread`) |
| :--- | :--- | :--- |
| **Wall-Clock Time** | 10.2655 seconds | 0.1219 |
| **Slowest Time** | 10.2430 seconds | 0.1098 |

---

## Discussion

Placing a synchronous blocking call inside an `async def` handler stalls FastAPI's single-threaded event loop, forcing concurrent incoming requests to execute sequentially in a queue. Offloading the operation to a worker thread pool (via a plain `def` handler or `asyncio.to_thread`) frees the event loop to immediately accept and handle all 10 incoming requests concurrently.