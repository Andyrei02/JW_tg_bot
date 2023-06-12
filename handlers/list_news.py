# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.


from utils.loader import dp
from utils.read_write_json import ReadWriteJson
from utils.config import LIST_NEWS_PATH


async def get_recommendation(path):
	rw_json = ReadWriteJson(path)

	return await rw_json.read()


async def public_list_news(message):
	dict_news_list = await get_recommendation(LIST_NEWS_PATH)

	await message.answer("O listă din ultimele știri:")

	if dict_news_list:
		for index in dict_news_list:
			text = f"<b>{dict_news_list[index]['title']}</b>\nData publicarii: {dict_news_list[index]['date']}\n<a href='{dict_news_list[index]['link']}'>🔗citește articolul</a>"
			await dp.bot.send_photo(message.chat.id, caption=text, photo=dict_news_list[index]['link'], parse_mode="HTML")
