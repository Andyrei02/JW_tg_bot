# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.


import asyncio

from utils.parser import NewsScraper, ListNewsScraper, DailyTextScraper, RecommendationScraper
from utils.read_write_json import ReadWriteJson
from utils.config import LAST_NEWS_PATH, LIST_NEWS_PATH, DAILY_TEXT_PATH, RECOMMENDATION_PATH


async def save_data(dict_data, path):
	rw_json = ReadWriteJson(path)

	await rw_json.start()
	await rw_json.write(dict_data)
	await rw_json.stop()


async def convert_list_to_dict(lst):
	return {i: d for i, d in enumerate(lst)}


async def update_data():

	news_scraper = NewsScraper("https://www.jw.org", "https://www.jw.org/ro/stiri/jw/")
	dict_news = await news_scraper.get_news()
	await save_data(dict_news, LAST_NEWS_PATH)

	daily_text_scraper = DailyTextScraper("https://wol.jw.org", "https://wol.jw.org/ro/wol/h/r34/lp-m/")
	dict_daily_text = await daily_text_scraper.get_daily_text()
	await save_data(dict_daily_text, DAILY_TEXT_PATH)

	recommendation_scraper = RecommendationScraper("https://www.jw.org", "https://www.jw.org/ro/")
	list_recommendation = await recommendation_scraper.get_recommendations()
	dict_recommendation = await convert_list_to_dict(list_recommendation)
	await save_data(dict_recommendation, RECOMMENDATION_PATH)

	# list_news_scraper = ListNewsScraper("https://www.jw.org/ro/stiri/jw/rss/NewsSubsectionRSSFeed/feed.xml")
	# list_news = await list_news_scraper.scrape()
	# print(list_news_scraper)
	# dict_news_list = await convert_list_to_dict(list_news)
	# await save_data(dict_news_list, LIST_NEWS_PATH)
