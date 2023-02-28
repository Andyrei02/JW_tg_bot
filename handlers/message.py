# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types

from utils.loader import dp
from utils.parse_site import get_news
from utils.users_database import UserDatabase
from utils import config



@dp.message_handler(state=None)
async def message(message: types.Message):
	# Echo the user's message back to them
	await message.answer(message.text)


async def parse_news(dp):
	dict_news = await get_news()
	if dict_news:
		await send_post(dict_news)


async def send_post(dict_news):
	title = dict_news["title"]
	link = dict_news["url"]
	intro = dict_news["intro"]
	caption = f"<b>{title}</b>\n{intro}...\n<a href='{link}'>open article</a>"
	
	db = UserDatabase(config.USER_DATABASE_URL)
	await db.connect()

	users = await db.get_all_users()
	if users:
		for user in users:
			await dp.bot.send_photo(user['chat_id'], caption=caption, photo=link, parse_mode="HTML")

	await db.close()
