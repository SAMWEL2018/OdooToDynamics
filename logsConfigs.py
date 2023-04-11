from datetime import datetime
from configs import Configs as cfg
import logging

import os


def log(level, msg):
    date = datetime.now().strftime("%Y%m%d")

    if not os.path.isdir(cfg().logsDir):
        os.makedirs(cfg().logsDir)

    logging.basicConfig(filemode='a', filename=cfg().logsDir + str(date) + '.log',
                        format='%(asctime)s - %(levelname)s -  %(message)s', force=True)

    print("Filepath: ", cfg().logsDir + str(date) + '.log')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    if (level == 1):
        logger.info(msg)
    elif (level == 2):
        logger.error(msg)
    elif (level == 3):
        logger.warning(msg)
    elif (level == 4):
        logger.debug(msg)
    else:
        print("Unknown Error Logging Level")
