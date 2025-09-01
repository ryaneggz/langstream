import sys
from loguru import logger

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>\n"
    "<level>{exception}</level>"  # Add exception/stacktrace to format
)


logger.remove()  # Remove the default handler
logger.add(
    sys.stdout,
    format=LOG_FORMAT,
    level="DEBUG",  # Change to DEBUG for verbose output
    colorize=True,
    backtrace=True,  # Show error backtraces for easier debugging
    # diagnose=True,   # Show variable values in tracebacks
    # catch=True,      # Catch exceptions and show full traceback
)

__all__ = ["logger"]
