import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)
logger = logging.getLogger("headshot_creator")
logger.DEBUG = "DEBUG"
