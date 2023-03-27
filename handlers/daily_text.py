# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types
from aiogram.dispatcher.filters import Command
import datetime

from utils.loader import dp
from utils.read_write_json import ReadWriteJson
from utils.config import DAILY_TEXT_PATH, USER_DATABASE_PATH
from utils.users_database import UserDatabase


async def get_daily_text(path):
	rw_json = ReadWriteJson(path)

	dict_daily_text = await rw_json.read()
	return dict_daily_text


@dp.message_handler(Command("daily_text"))
async def handler_public_daily_text(message: types.Message):
	dict_text = await get_daily_text(DAILY_TEXT_PATH)

	async with aiofiles.open("media/verses_img.jpg", "rb") as f:
		photo_verses = await f.read()


	text = f"""
	<b>{dict_text["title"]}</b>
	<b>{dict_text["verse"]}</b>
			"""

	await dp.bot.send_photo(message.chat.id, caption=text, photo=photo_verses, parse_mode="HTML")
	await message.answer(dict_text["body"], parse_mode="HTML")

	await message.delete()


async def public_daily_text():
	dict_text = await get_daily_text(DAILY_TEXT_PATH)

	async with aiofiles.open("media/verses_img.jpg", "rb") as f:
		photo_verses = await f.read()


	text = f"""
	<b>{dict_text["title"]}</b>
	<b>{dict_text["verse"]}</b>
			"""

	db = UserDatabase(USER_DATABASE_PATH)
	await db.connect()

	users = await db.get_all_users()
	if users:
		for user in users:
			await dp.bot.send_photo(user['chat_id'], caption=text, photo=photo_verses, parse_mode="HTML")
			await dp.bot.send_message(user['chat_id'], dict_text["body"], parse_mode="HTML")

	await db.close()
