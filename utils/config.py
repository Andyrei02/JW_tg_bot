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

USER_DATABASE_NAME = "users_data.db"
USER_DATABASE_PATH = f"data/{USER_DATABASE_NAME}"
LAST_NEWS_NAME = "last_news.json"
LAST_NEWS_PATH = f"data/{LAST_NEWS_NAME}"
DAILY_TEXT_NAME = "daily_text.json"
DAILY_TEXT_PATH = f"data/{DAILY_TEXT_NAME}"

DEBUG = True