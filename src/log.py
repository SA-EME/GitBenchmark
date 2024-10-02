"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""


import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import colorlog

from env import LOG_LEVEL, LOG_FILE

try:
    level = logging.getLevelName(LOG_LEVEL.upper())
    logging.basicConfig(level=level)
    logger = logging.getLogger()
    logger.handlers = []

    logger.setLevel(level)

    formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(levelname)s] %(reset)s %(asctime)s\t(%(filename)s)\t%(message)s',
        reset=True,
        style='%',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        })

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if LOG_FILE:
        log_path = os.path.join(os.getcwd())
        file_handler = RotatingFileHandler(
            os.path.join(log_path, 'app.log'),
            maxBytes=100000000,
            backupCount=3
        )
        file_handler.setFormatter(logging.Formatter(
            '[%(levelname)s]\t %(asctime)s\t(%(filename)s)\t%(message)s'))
        logger.addHandler(file_handler)

except Exception as ex:
    print(ex)
    sys.exit(1)
