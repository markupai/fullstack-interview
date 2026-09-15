# backend

One Python package, two run roles:

```
uv run python -m app.main api      # FastAPI on :8000
uv run python -m app.main worker   # Temporal worker
```

Both need a Temporal server at `TEMPORAL_ADDRESS` (default `localhost:7233`).
See the repo root README for the full setup.
