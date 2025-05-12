import sys
from loguru import logger
from pathlib import Path


def init_logger():
    """
    Initializes the Loguru logger:
    - removes default handler
    - adds file + console handlers
    - sets colors for log levels
    """
    logs_path = Path("logger/logs")
    logs_path.mkdir(parents=True, exist_ok=True)

    logger.remove()

    # File output
    logger.add(
        logs_path / "logs.log",
        rotation="100 MB",
        compression="zip",
        retention="30 days",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{line} | {message}",
        level="DEBUG",
    )

    # Console output
    logger.add(
        sys.stdout,
        colorize=True,
        format="<b><e>{time:YYYY-MM-DD at HH:mm:ss}</e></b> | <c>{level}</c> | {file}:{line} | <level>{message}</level>",
        level="DEBUG",
    )

    # Level-specific color settings
    logger.level("INFO", color="<m>")
    logger.level("CRITICAL", color="<v><r><bold>")
    logger.level("DEBUG", color="<c>")
    logger.level("WARNING", color="<y><bold>")
    logger.level("ERROR", color="<r><bold>")

    logger.info("🔧 Logger successfully initialized.")
