# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types
from aiogram.dispatcher.filters import Command
import datetime

from utils.loader import dp

import xml.etree.ElementTree as ET
import urllib.request


@dp.message_handler(Command("list_news"))
async def manage_news(message: types.Message):
	list_news = await get_list_news()

	await message.answer("Lista Știrilor:")

	for news in list_news[::-1]:
		text = f"<b>{news[1]}</b>\nData publicarii: {await convert_date_to_romanian(news[2])}\n<a href='{news[0]}'>🔗citește articolol</a>"
		await dp.bot.send_photo(message.chat.id, caption=text, photo=news[0], parse_mode="HTML")


async def convert_date_to_romanian(date_str):
	# Parse the English date string into a datetime object
	date = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
	# Define the Romanian month names
	months = [
		'ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie',
		'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie'
	]
	# Format the datetime object as a Romanian date string
	romanian_date_str = f"{date.day} {months[date.month - 1]} {date.year}"
	return romanian_date_str


async def get_list_news():
	url = "https://www.jw.org/ro/stiri/jw/rss/NewsSubsectionRSSFeed/feed.xml"
	xml_data = urllib.request.urlopen(url).read()

	# Parse the XML data
	root = ET.fromstring(xml_data)
	list_news = []

	# Iterate over each news item and print the title and link
	for item in root.iter("item"):
		title = item.find("title").text
		link = item.find("link").text
		date = item.find("pubDate").text
		list_news.append([link, title, date])

	return list_news
