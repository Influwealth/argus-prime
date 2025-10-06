import os
import sys
import logging
from agents.mindmax.api import MindMaxAPI

logging.basicConfig(level=logging.INFO)

def start_mindmax_service():
    """Initializes and starts the MindMax API service."""
    try:
        logging.info("Starting MindMax vGPU Core Service...")
        api = MindMaxAPI()
        logging.info(f"MindMax core running. PID: {os.getpid()}")
        while True:
            pass
    except Exception as e:
        logging.error(f"FATAL: Failed to start MindMax core: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    start_mindmax_service()
