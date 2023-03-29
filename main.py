# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import logging
import os
import aioschedule
import asyncio
from aiogram import executor

from utils.loader import dp
import handlers
from utils.update_data import update_data


logging.basicConfig(level=logging.INFO)


async def scheduler(dp):
	try:
		aioschedule.every().day.at("4:40").do(handlers.daily_news.update_data)
		aioschedule.every().day.at("5:00").do(handlers.daily_text.public_daily_news)
		aioschedule.every().day.at("6:00").do(handlers.daily_text.public_daily_text)
		while True:
			await aioschedule.run_pending()
			await asyncio.sleep(1)
	except Exception as e:
		print(f"\nERROR: {e}\n")


async def on_startup(dispatcher):
	asyncio.create_task(scheduler(dispatcher))
	await update_data()


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
