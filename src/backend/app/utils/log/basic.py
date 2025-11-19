import logging
import structlog
import os
from logging.handlers import RotatingFileHandler

def create_logger():
    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    # --- Base logging ---
    logger_name = "INT3505E_2_demo"
    root_logger = logging.getLogger(logger_name)
    root_logger.setLevel(level=logging.INFO)

    # File handler
    file_handler = RotatingFileHandler(
        "logs/INT3505E_2_demo.logs.jsonl",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # --- Structlog setup ---
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ]
            ),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger(logger_name)

# def clean_loggers_hell():
#     # --- Configure root logger to use only these handlers (no other handlers leaking) ---
#     root_logger = logging.getLogger()
#     # Remove ALL existing handlers to avoid duplicate/text logs
#     for h in list(root_logger.handlers):
#         root_logger.removeHandler(h)

#     root_logger.handlers = []          # remove everything
#     root_logger.propagate = False

#     # Disable werkzeug request logs
#     logging.getLogger("werkzeug").disabled = True

#     # Disable flask default exception logging
#     logging.getLogger("flask.app").propagate = False
#     logging.getLogger("flask.app").disabled = True

# clean_loggers_hell()
log = create_logger()
log.info("Logger initialized properly")
