CREATE TABLE IF NOT EXISTS metrics (
  id BIGSERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  source TEXT NOT NULL,
  cpu_util NUMERIC(5,2) NOT NULL,
  mem_util NUMERIC(5,2) NOT NULL,
  latency_ms NUMERIC(7,2) NOT NULL,
  error_rate NUMERIC(5,2) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_metrics_ts ON metrics (ts DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_source_ts ON metrics (source, ts DESC);
