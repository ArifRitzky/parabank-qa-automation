import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from runner import run_suite

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="QA Dashboard API")
_run_lock = threading.Lock()


@app.post("/run-test")
def run_tests():
    """Run the whole suite and return per-test results. Only one run at a time."""
    if not _run_lock.acquire(blocking=False):
        raise HTTPException(status_code=409, detail="A test run is already in progress")
    try:
        return run_suite()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        _run_lock.release()


# The dashboard is served by the same app, so it needs no CORS configuration.
(ROOT / "screenshots").mkdir(exist_ok=True)
app.mount("/screenshots", StaticFiles(directory=ROOT / "screenshots"), name="screenshots")
app.mount("/", StaticFiles(directory=ROOT / "frontend", html=True), name="frontend")
