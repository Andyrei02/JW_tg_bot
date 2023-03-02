# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import os
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if TELEGRAM_TOKEN is None:
	raise ValueError("Telegram API token not found in environment variables")

if not os.path.exists('data'): os.mkdir('data')

USER_DATABASE_NAME = "data.db"
USER_DATABASE_URL = f"data/{USER_DATABASE_NAME}"

DEBUG = True