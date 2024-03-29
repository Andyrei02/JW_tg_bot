# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import aiofiles

from utils.loader import dp, db
from utils.read_write_json import ReadWriteJson
from utils.config import DAILY_TEXT_PATH


async def get_daily_text(path):
	rw_json = ReadWriteJson(path)

	dict_daily_text = await rw_json.read()
	return dict_daily_text

async def public_daily_text(chat_id=None):
	dict_text = await get_daily_text(DAILY_TEXT_PATH)

	async with aiofiles.open("media/verses_img.jpg", "rb") as f:
		photo_verses = await f.read()

	await send_post(dict_text, photo_verses, chat_id)


async def send_post(dict_text, photo_verses, user=None):
	text = f"""
	<b>{dict_text["title"]}</b>
	<b>{dict_text["verse"]}</b>
			"""

	if user:
		await dp.bot.send_photo(user, caption=text, photo=photo_verses, parse_mode="HTML")
		await dp.bot.send_message(user, dict_text["body"], parse_mode="HTML")
	else:
		await db.connect()

		users = await db.get_all_users()
		if users:
			for user in users:
				await dp.bot.send_photo(user['chat_id'], caption=text, photo=photo_verses, parse_mode="HTML")
				await dp.bot.send_message(user['chat_id'], dict_text["body"], parse_mode="HTML")

		await db.close()
