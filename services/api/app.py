import asyncio
import os
from datetime import datetime, timedelta
from typing import Optional

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_URL = os.getenv("DATABASE_URL")
PORT = int(os.getenv("UVICORN_PORT", "8000"))

app = FastAPI(title="InsightHub API", version="0.1.0")

class MetricIn(BaseModel):
    source: str
    cpu_util: float
    mem_util: float
    latency_ms: float
    error_rate: float

@app.on_event("startup")
async def startup():
    # Try a few times for the DB to be ready, then continue anyway.
    retries = 10
    for i in range(retries):
        try:
            async with await psycopg.AsyncConnection.connect(DB_URL) as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 1")
            print("✅ DB connection OK")
            return
        except Exception as e:
            print(f"⏳ DB not ready yet ({i+1}/{retries}): {e}")
            await asyncio.sleep(3)

    print("⚠️ DB still not ready after retries; API will start anyway.")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/metrics")
async def ingest_metric(m: MetricIn):
    try:
        async with await psycopg.AsyncConnection.connect(DB_URL) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO metrics (source, cpu_util, mem_util, latency_ms, error_rate)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, ts
                    """,
                    (m.source, m.cpu_util, m.mem_util, m.latency_ms, m.error_rate),
                )
                row = await cur.fetchone()
                await conn.commit()
                return {"id": row[0], "ts": row[1].isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/latest")
async def latest(limit: int = 100, source: Optional[str] = None):
    q = "SELECT ts, source, cpu_util, mem_util, latency_ms, error_rate FROM metrics"
    params = []
    if source:
        q += " WHERE source = %s"
        params.append(source)
    q += " ORDER BY ts DESC LIMIT %s"
    params.append(limit)

    async with await psycopg.AsyncConnection.connect(DB_URL) as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            rows = await cur.fetchall()
            return [
                {
                    "ts": r[0].isoformat(),
                    "source": r[1],
                    "cpu_util": float(r[2]),
                    "mem_util": float(r[3]),
                    "latency_ms": float(r[4]),
                    "error_rate": float(r[5]),
                }
                for r in rows
            ]

@app.get("/metrics/series")
async def series(
    minutes: int = 15,
    source: Optional[str] = None,
):
    since = datetime.utcnow() - timedelta(minutes=minutes)
    q = (
        "SELECT ts, source, cpu_util, mem_util, latency_ms, error_rate "
        "FROM metrics WHERE ts >= %s"
    )
    params = [since]
    if source:
        q += " AND source = %s"
        params.append(source)
    q += " ORDER BY ts ASC"

    async with await psycopg.AsyncConnection.connect(DB_URL) as conn:
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            rows = await cur.fetchall()
            return [
                {
                    "ts": r[0].isoformat(),
                    "source": r[1],
                    "cpu_util": float(r[2]),
                    "mem_util": float(r[3]),
                    "latency_ms": float(r[4]),
                    "error_rate": float(r[5]),
                }
                for r in rows
            ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
