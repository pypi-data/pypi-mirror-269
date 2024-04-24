from ...itakello_logging import ItakelloLogging

logger = ItakelloLogging().get_logger(__name__)


def test_func() -> None:
    logger.debug("Test debug message from test.py")
    logger.info("Test info message from test.py")
    logger.confirmation("Test confirmation message from test.py")
    logger.warning("Test warning message from test.py")
    logger.error("Test error message from test.py")
    logger.critical("Test critical message from test.py")
