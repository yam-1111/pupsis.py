import logging
import warnings
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

class Logger(logging.Logger):
    def __init__(self, name, level=None, log_file=None):
        if level is None:
            self.disabled = True  # Disable logging if level is None
            return

        super().__init__(name, level)
        self.extra_info = None

        # Console handler with color formatting
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s - %(asctime)s] - %(message)s')
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)

        # File handler (optional, without colors)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.addHandler(file_handler)

    def format_message(self, level, msg):
        """Applies color based on log level"""
        color_map = {
            "INFO": Fore.CYAN,
            "DEBUG": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.MAGENTA,
        }
        color = color_map.get(level, "")
        return f"{color}{msg}{Style.RESET_ALL}"

    def info(self, msg, *args, **kwargs):
        if self.disabled:
            return
        super().info(self.format_message("INFO", msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.disabled:
            return
        super().debug(self.format_message("DEBUG", msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Logs a warning message in yellow and also issues a Python warning."""
        if self.disabled:
            return
        warnings.warn(msg, UserWarning)  # Issue a Python warning
        super().warning(self.format_message("WARNING", msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
 
        if self.disabled:
            return
        super().error(self.format_message("ERROR", msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.disabled:
            return
        super().critical(self.format_message("CRITICAL", msg), *args, **kwargs)
