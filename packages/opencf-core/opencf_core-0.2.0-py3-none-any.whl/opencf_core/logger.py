from loguru import logger


def setup_logger(log_file="logs/app.log"):
    """
    Setup logger configuration.
    """
    # logger.remove()  # Remove default configuration
    logger.add(
        log_file,
        rotation="10 MB",  # Rotate log file when it reaches 10 MB
        retention="7 days",  # Keep logs for 7 days
        level="DEBUG",  # Log level
    )
    # logger.add(  # Add console output
    #     sink=lambda message: print(message),  # Print log messages to console
    #     level="INFO",  # Log level
    # )


setup_logger()  # Setup logger when the module is imported
