import structlog
import logging
import sys

def configure_logging(log_level="INFO"):
    """
    Configures structured JSON logging for the agent.
    This ensures that logs are machine-readable, which is essential for observable systems.
    """
    # Configure standard logging to output to stdout
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    structlog.configure(
        processors=[
            # Filter logs by level (debug, info, error)
            structlog.stdlib.filter_by_level,
            # Add logger name and log level to the output
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            # Allow positional arguments in log calls
            structlog.stdlib.PositionalArgumentsFormatter(),
            # Add ISO timestamp
            structlog.processors.TimeStamper(fmt="iso"),
            # Add stack info for exceptions
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # Render the final output as JSON
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
