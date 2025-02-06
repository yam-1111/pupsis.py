import logging

class Logger(logging.Logger):
    def __init__(self, name, level=None, log_file=None):
        if level is None:
            self.disabled = True  # Disable logging if level is None
            return

        super().__init__(name, level)
        self.extra_info = None

        # Console handler
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s - %(asctime)s] - %(message)s')
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)

        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.addHandler(file_handler)

    def info(self, msg, *args, **kwargs):
        if self.disabled:
            return  # Skip logging if disabled
        super().info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.disabled:
            return  # Skip logging if disabled
        super().debug(msg, *args, **kwargs)
