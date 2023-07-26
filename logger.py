import logging


class Logger:
    def __init__(self):
        self._logger = logging.getLogger("default")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)

    @property
    def logger(self):
        return self._logger
