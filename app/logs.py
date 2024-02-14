import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    log_level = logging.INFO

    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configure the root logger
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=10)])

    # Example to configure logging for a specific library if needed
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Call setup_logging() at the start of your application
# setup_logging()
