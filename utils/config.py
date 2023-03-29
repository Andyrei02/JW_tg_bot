# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import os
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

if TELEGRAM_TOKEN is None:
	raise ValueError("Telegram API token not found in environment variables")

if not os.path.exists('data'): os.mkdir('data')

LAST_NEWS_NAME = "last_news.json"
LAST_NEWS_PATH = f"data/{LAST_NEWS_NAME}"
DAILY_TEXT_NAME = "daily_text.json"
DAILY_TEXT_PATH = f"data/{DAILY_TEXT_NAME}"

db_host = os.getenv('MYSQLHOST')
db_port = os.getenv('MYSQLPORT')
db_database = os.getenv('MYSQLDATABASE')
db_username = os.getenv('MYSQLUSER')
db_password = os.getenv('MYSQLPASSWORD')

db_config = {
	'user': db_username,
	'password': db_password,
	'host': db_host,
	'port': db_port,
	'database': db_database
}

DEBUG = True