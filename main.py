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

from utils.loader import bot, dp
import handlers


logging.basicConfig(level=logging.INFO)


async def scheduler(dp):
	try:
		aioschedule.every().day.at("5:00").do(handlers.message.parse_news, dp)
		while True:
			await aioschedule.run_pending()
			await asyncio.sleep(1)
	except Exception as e:
		print(f"\nERROR: {e}\n")


async def on_startup(dispatcher):
	asyncio.create_task(scheduler(dispatcher))


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
