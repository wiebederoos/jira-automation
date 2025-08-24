# logging_config.py
import os
import logging
from constants import LOG_FILE

def configure_logging():
    """Configures logging based on the log level from the environment variables."""
    
    # Read the log level from the environment variable, default to INFO if not set
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Mapping for log level strings to logging constants
    log_level_dict = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    # Set default log level if it's invalid
    level = log_level_dict.get(log_level, logging.INFO)

    # Configure the root logger to write to the app.log file
    logging.basicConfig(
        filename=LOG_FILE,
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'  # append mode
    )

    # Also, log to the console (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)
