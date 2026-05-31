import os
import sys
import logging
import uvicorn
from agents.mindmax.api import MindMaxAPI

logging.basicConfig(level=logging.INFO)

def start_mindmax_service():
    """Initializes and starts the MindMax API service."""
    try:
        logging.info("Starting MindMax vGPU Core Service...")
        api = MindMaxAPI()
        host = os.environ.get("HOST", "0.0.0.0")
        port = int(os.environ.get("PORT", "8080"))
        logging.info(f"MindMax core running on {host}:{port}. PID: {os.getpid()}")
        uvicorn.run(api, host=host, port=port)
    except Exception as e:
        logging.error(f"FATAL: Failed to start MindMax core: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    start_mindmax_service()
