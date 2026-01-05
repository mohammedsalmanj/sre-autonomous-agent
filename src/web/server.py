from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import psutil
import structlog
from typing import List, Dict, Any

# Create a simple in-memory log buffer for the demo
# In production, use a proper database or log aggregator
log_buffer: List[Dict[str, Any]] = []

def get_log_buffer():
    return log_buffer

# Custom Logger Processor to intercept logs and save to buffer
def buffer_processor(logger, method_name, event_dict):
    # Keep only last 50 logs
    if len(log_buffer) > 50:
        log_buffer.pop(0)
    log_buffer.append(event_dict.copy())
    return event_dict

# Re-configure logging to include our buffer processor
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        # Our custom processor to capture logs for UI
        buffer_processor,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=False, # Disable cache so config takes effect
)

app = FastAPI()

# Mount static files (our HTML)
import os
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/dashboard", StaticFiles(directory=static_path, html=True), name="static")

@app.get("/")
def read_root():
    return {"status": "SRE Agent Online", "dashboard_url": "/dashboard"}

@app.get("/api/stats")
def get_stats():
    return {
        "system": {
            "cpu": psutil.cpu_percent(interval=None),
            "memory": psutil.virtual_memory().percent
        }
    }

@app.get("/api/logs")
def get_logs():
    return log_buffer
