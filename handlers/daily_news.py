# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from utils.loader import dp, db
from utils.read_write_json import ReadWriteJson
from utils.config import LAST_NEWS_PATH


async def get_daily_news(path):
	rw_json = ReadWriteJson(path)

	dict_daily_text = await rw_json.read()
	return dict_daily_text


async def public_daily_news(chat_id=None):
	dict_news = await get_daily_news(LAST_NEWS_PATH)

	if dict_news:
		await send_post(dict_news, chat_id)


async def send_post(dict_news, user=None):
	title = dict_news["title"]
	link = dict_news["url"]
	intro = dict_news["intro"]
	caption = f"<b>{title}</b>\n{intro}...\n<a href='{link}'>citește articolul</a>"
	
	if user:
		await dp.bot.send_photo(user, caption=caption, photo=link, parse_mode="HTML")
	else:
		await db.connect()

		users = await db.get_all_users()
		if users:
			for user in users:
				await dp.bot.send_photo(user['chat_id'], caption=caption, photo=link, parse_mode="HTML")

		await db.close()
