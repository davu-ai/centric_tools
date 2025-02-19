import logging


class CustomLogger:
    logger = logging.getLogger("centric_tool")
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(context)s"
    )
    ch.setFormatter(formatter)

    @classmethod
    def info(cls, message: str, context: dict = None):
        context = context or {}
        cls.logger.setLevel(logging.INFO)
        cls.ch.setLevel(logging.INFO)

        # Add the handler to the logger
        if not cls.logger.hasHandlers():
            cls.logger.addHandler(cls.ch)

        # Log the message along with the context
        cls.logger.info(message, extra={"context": context})
