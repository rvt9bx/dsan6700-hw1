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
| **Wall-Clock Time** | 10.2655 sec | 1.0278 sec |
| **Slowest Time** | 10.2430 sec | 1.0270 sec |

---

## Discussion

Placing a synchronous blocking call inside an `async def` handler stalls FastAPI's single-threaded event loop, forcing concurrent incoming requests to execute sequentially in a queue. Offloading the operation to a worker thread pool (via a plain `def` handler or `asyncio.to_thread`) frees the event loop to immediately accept and handle all 10 incoming requests concurrently.

---

# Docker Image Metrics

## Image Size

| Metric | Value |
| :--- | :--- |
| **Image size on disk** | 9.3 GB (`docker images` reports 9.301GB) |

## Rebuild Time After a One-Line Code Change

| Build Type | Time |
| :--- | :--- |
| **With cached dependency layer** (`uv sync` layer reused) | ~3.0 seconds |
| **No cache** (`docker build --no-cache`, full clean build) | ~3 minutes 11.6 seconds (191.6s) |

## docker system df (stack running)

```
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          1         1         9.301GB   0B (0%)
Containers      1         1         32.77kB   0B (0%)
Local Volumes   1         1         0B        0B
Build Cache     29        0         19.31GB   9.73GB
```

## Discussion

Caching the dependency-install layer (`uv sync --frozen --no-dev --no-install-project`, run before the source is copied) makes the rebuild roughly 64x faster: a one-line source change only reruns the final `uv sync` step and image export, since nothing upstream of `COPY src ./src` in the Dockerfile changed. A full `--no-cache` build reruns every layer from scratch, including a ~48-second dependency download and install plus apt package installation.

The image's 9.3GB size comes from `sentence-transformers`'s dependency on full GPU-enabled PyTorch (`torch`, `nvidia-cublas`, `nvidia-cudnn`, `triton`, and related packages), even though this service only runs a small CPU-bound model (`all-MiniLM-L6-v2`) and Jetstream2's `m3.medium` instance has no GPU. A CPU-only torch build would substantially reduce this.