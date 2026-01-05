import sys
import os

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import threading
import uvicorn
from core.engine import AgentEngine
from logger import configure_logging
# Import the FastApi app to run it
from web.server import app

def run_web_server():
    """Runs the FastAPI server."""
    # Run slightly different port to avoid conflicts
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

def main():
    # 1. Initialize Logging
    # We configure it in web.server too for capturing logs, 
    # but calling it here ensures basic stdout setup.
    configure_logging(log_level="INFO")
    
    # 2. Start Web Server in a background thread
    # Daemon=True means it will die when the main thread dies
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    
    print("\n" + "="*50)
    print(" SRE AGENT DASHBOARD: http://localhost:8000/dashboard")
    print("="*50 + "\n")
    
    # 3. Initialize the Engine
    # default to 5 second loop for dev
    engine = AgentEngine(interval_seconds=5)
    
    # 4. Start the Agent (Main Thread)
    # This captures the main thread so Ctrl+C works on the engine
    try:
        engine.start()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
