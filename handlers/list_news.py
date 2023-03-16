# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types
from aiogram.dispatcher.filters import Command
import datetime

from utils.loader import dp
from utils.parser import ListNewsScraper


@dp.message_handler(Command("list_news"))
async def public_list_news(message: types.Message):
	scraper = ListNewsScraper("https://www.jw.org/ro/stiri/jw/rss/NewsSubsectionRSSFeed/feed.xml")
	news_list = await scraper.scrape()

	await message.answer("Lista Știrilor:")

	for news in news_list:
		text = f"<b>{news['title']}</b>\nData publicarii: {news['date']}\n<a href='{news['link']}'>🔗citește articolul</a>"
		await dp.bot.send_photo(message.chat.id, caption=text, photo=news['link'], parse_mode="HTML")
