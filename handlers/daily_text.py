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
from utils.config import DAILY_TEXT_PATH


async def get_daily_text(path):
	rw_json = ReadWriteJson(path)

	dict_daily_text = await rw_json.read()
	return dict_daily_text


@dp.message_handler(Command("daily_text"))
async def handler_public_daily_text(message: types.Message):
	dict_text = await get_daily_text(DAILY_TEXT_PATH)

	photo_verses = open("data/verses_img.jpg", "rb")

	text = f"""
	<b>{dict_text["title"]}</b>
	<b>{dict_text["verse"]}</b>
			"""

	await dp.bot.send_photo(message.chat.id, caption=text, photo=photo_verses, parse_mode="HTML")
	await message.answer(dict_text["body"], parse_mode="HTML")


async def public_daily_text():
	dict_text = await get_daily_text(DAILY_TEXT_PATH)

	photo_verses = open("data/verses_img.jpg", "rb")

	text = f"""
	<b>{dict_text["title"]}</b>
	<b>{dict_text["verse"]}</b>
			"""

	await dp.bot.send_photo(message.chat.id, caption=text, photo=photo_verses, parse_mode="HTML")
	await message.answer(dict_text["body"], parse_mode="HTML")