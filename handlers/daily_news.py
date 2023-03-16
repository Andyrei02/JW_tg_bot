# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types
from aiogram.dispatcher.filters import Command
import datetime

from utils.users_database import UserDatabase
from utils.loader import dp
from utils.read_write_json import ReadWriteJson
from utils.config import LAST_NEWS_PATH, USER_DATABASE_PATH


async def get_daily_news(path):
	rw_json = ReadWriteJson(path)

	dict_daily_text = await rw_json.read()
	return dict_daily_text


@dp.message_handler(Command("daily_news"))
async def handler_public_daily_news(message: types.Message):
	dict_news = await get_daily_news(LAST_NEWS_PATH)

	if dict_news:
		await send_post(dict_news)


async def public_daily_news():
	dict_news = await get_daily_news(LAST_NEWS_PATH)

	if dict_news:
		await send_post(dict_news)


async def send_post(dict_news):
	title = dict_news["title"]
	link = dict_news["url"]
	intro = dict_news["intro"]
	caption = f"<b>{title}</b>\n{intro}...\n<a href='{link}'>citește articolul</a>"
	
	db = UserDatabase(USER_DATABASE_PATH)
	await db.connect()

	users = await db.get_all_users()
	if users:
		for user in users:
			await dp.bot.send_photo(user['chat_id'], caption=caption, photo=link, parse_mode="HTML")

	await db.close()