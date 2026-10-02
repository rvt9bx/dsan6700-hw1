import asyncio
import time
import httpx

URL = "http://127.0.0.1:8000/predict"
PAYLOAD = {"text": "testing blocking behavior"}
NUM_REQUESTS = 10

async def send_request(client: httpx.AsyncClient, req_id: int) -> float:
    start = time.perf_counter()
    response = await client.post(URL, json=PAYLOAD)
    duration = time.perf_counter() - start
    print(
        f"Request {req_id} finished in {duration:.4f}s with status {response.status_code}"
    )
    return duration

async def main():
    async with httpx.AsyncClient(timeout=None) as client:
        start_wall = time.perf_counter()
        durations = await asyncio.gather(
            *(send_request(client, i) for i in range(NUM_REQUESTS))
        )
        total_wall_time = time.perf_counter() - start_wall

    print("\n--- RESULTS ---")
    print(f"Total Time: {total_wall_time:.4f} seconds")
    print(f"Slowest Request Time:  {max(durations):.4f} seconds")

if __name__ == "__main__":
    asyncio.run(main())