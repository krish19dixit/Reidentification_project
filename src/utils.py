import logging
import os

def setup_logging(log_level=logging.INFO):
    """Setup logging configuration"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('player_reidentification.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)