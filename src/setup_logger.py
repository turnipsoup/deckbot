import logging ,json, sys, os
from logging.handlers import RotatingFileHandler


# Load config file
config_dir = './config'
config = json.loads(open(f"{config_dir}/config.json", "r").read())


# If we have a logging directory defined and if it is not blank, then use a 
# RotatingFileHandler as well.
if config["logging_directory"]:
    if config["logging_directory"] != '':

        # Make log directory if it does not exist:
        if os.path.isdir(config['logging_directory']):
            pass
        else:
            os.mkdir(config['logging_directory'])


        # Configure logging
        logging.root.handlers = []
        logging.basicConfig(
            level=config['logging_level'],
            format="%(asctime)s|%(levelname)s|%(message)s",
            handlers=[
                RotatingFileHandler(f'{config["logging_directory"]}/app.log', maxBytes=config['logging_max_file_size'], backupCount=config['logging_backup_count']),
                logging.StreamHandler(sys.stdout)
            ])

    else:
        logging.root.handlers = []
        logging.basicConfig(
            level=config['logging_level'],
            format="%(asctime)s|%(levelname)s|%(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout)
            ])


logger = logging.getLogger('mainlogger')