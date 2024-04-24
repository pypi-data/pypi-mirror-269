import logging


class ConsoleFormatter(logging.Formatter):
    """Custom formatter to add colors to logging levels."""

    CONFIRMATION_LEVEL = 25
    INSTRUCTION_LEVEL = 24

    color_codes = {
        logging.DEBUG: "\033[94m",  # Blue
        CONFIRMATION_LEVEL: "\033[92m",  # Green
        INSTRUCTION_LEVEL: "\033[36m",  # Orange
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }

    def format(self, record):
        level_color = self.color_codes.get(
            record.levelno, "\033[0m"
        )  # Default to no color
        message = super().format(record)
        return f"{level_color}{message}\033[0m"  # Reset to default color at the end
