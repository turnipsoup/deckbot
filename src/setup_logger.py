import logging,json, sys
from logging.handlers import RotatingFileHandler


# Load config file
config_dir = './config'
config = json.loads(open(f"{config_dir}/config.json", "r").read())

# Configure logging
logging.root.handlers = []
logging.basicConfig(
    level=config['logging_level'],
    format="%(asctime)s|%(levelname)s|%(message)s",
    handlers=[
        RotatingFileHandler(f'{config["logging_directory"]}/app.log', maxBytes=config['logging_max_file_size'], backupCount=config['logging_backup_count']),
        logging.StreamHandler(sys.stdout)
    ])

logger = logging.getLogger('mainlogger')