# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from utils.loader import dp, db
from utils.read_write_json import ReadWriteJson
from utils.config import RECOMMENDATION_PATH


async def get_recommendation(path):
	rw_json = ReadWriteJson(path)

	return await rw_json.read()


async def public_recommendation(chat_id=None):
	dict_recommendation = await get_recommendation(RECOMMENDATION_PATH)

	if dict_recommendation:
		for index in dict_recommendation:
			await send_post(dict_recommendation[index], user=chat_id)


async def send_post(dict_recommendation, user=None):
	title = dict_recommendation["title"]
	link = dict_recommendation["link"]
	img = dict_recommendation["img"]
	caption = f"<a href='{link}'>{title}</a>"
	
	if user:
		await dp.bot.send_photo(user, caption=caption, photo=img, parse_mode="HTML")
	else:
		await db.connect()

		users = await db.get_all_users()
		if users:
			for user in users:
				await dp.bot.send_photo(user, caption=caption, photo=img, parse_mode="HTML")

		await db.close()
