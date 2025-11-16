import os, asyncio, math, random
import httpx

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
INTERVAL = float(os.getenv("INTERVAL_SECONDS", 2))
SOURCES = ["web-1", "api-1", "worker-1"]

async def push_once(client: httpx.AsyncClient, source: str, t: float):
    cpu = max(0, min(100, 55 + 35*math.sin(t/15.0) + random.gauss(0, 8)))
    mem = max(0, min(100, 40 + 25*math.sin(t/23.0 + 1) + random.gauss(0, 6)))
    latency = max(1, 80 + 40*math.sin(t/10.0) + abs(random.gauss(0, 20)))
    err = max(0, min(100, abs(random.gauss(2, 1)) + (8 if random.random()<0.05 else 0)))
    payload = {
        "source": source,
        "cpu_util": round(cpu, 2),
        "mem_util": round(mem, 2),
        "latency_ms": round(latency, 2),
        "error_rate": round(err, 2)
    }
    r = await client.post(f"{API_BASE}/metrics", json=payload, timeout=10)
    r.raise_for_status()

async def main():
    async with httpx.AsyncClient() as client:
        t = 0.0
        while True:
            for s in SOURCES:
                try:
                    await push_once(client, s, t)
                except Exception as e:
                    print("push failed:", e)
            await asyncio.sleep(INTERVAL)
            t += INTERVAL

if __name__ == "__main__":
    asyncio.run(main())
