# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import logging

# Create a logger
logger = logging.getLogger("my_bot_logger")
logger.setLevel(logging.DEBUG)

# Create a file handler and set the log level to INFO
fh = logging.FileHandler("my_bot.log")
fh.setLevel(logging.INFO)

# Create a console handler and set the log level to DEBUG
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
