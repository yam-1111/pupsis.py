
import logging


class Logger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG, log_file=None):
        super().__init__(name, level)
        self.extra_info = None

        # Console handler
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s - %(asctime)s]  - %(message)s')
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)

        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.addHandler(file_handler)

    def info(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        super().info(msg, *args, extra=extra_info, **kwargs)
    



    