# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import requests
from bs4 import BeautifulSoup

import asyncio
import aiohttp
from utils import save_last_news
from utils.config import LAST_NEWS_PATH


async def get_site_page(link):
	async with aiohttp.ClientSession() as session:
		async with session.get(link) as resp:
			response =  await resp.text()
	return BeautifulSoup(response, 'lxml')


async def get_last_news_block(soup):
	block = soup.find(class_="landingPagePrimaryFeature")
	block = block.find(class_="presentationIntent-desktop")
	return block


async def get_img(block):
	img_block = block.find(class_="syn-img pnr")
	return img_block.find("img")["src"]


async def get_title(block):
	title_block = block.find(class_="syn-body pnr")
	title = title_block.find("h3").text
	return title


async def get_url(block, source_link):
	url_block = block.find(class_="syn-body pnr")
	url = source_link + url_block.find("a")["href"]
	return url


async def get_introduction(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			response =  await resp.text()

	content_page = BeautifulSoup(response, 'lxml')
	content_block = content_page.find(class_="contentBody")
	pGroup = content_block.find(class_="pGroup")
	intro = "\n" + content_block.find(class_="p2").text

	return intro


async def get_dict_news(source_link, news_link):
	soup = await get_site_page(news_link)
	block = await get_last_news_block(soup)
	img = await get_img(block)
	title = await get_title(block)
	url = await get_url(block, source_link)
	intro = await get_introduction(url)

	return {"img": img, "title": title.strip(), "intro": intro, "url": url}


async def get_news():
	source_link = 'https://www.jw.org'
	news_link = 'https://www.jw.org/ro/stiri/jw/'

	dict_news = await get_dict_news(source_link, news_link)

	rw_json = save_last_news.ReadWriteJson(LAST_NEWS_PATH)
	await rw_json.start()

	try:
		last_news = await rw_json.read()
		if last_news != dict_news:
			return dict_news

	except FileNotFoundError:
		return dict_news

	except Exception as e:
		print(f"\nERROR: {e}\n")

	finally:
		await rw_json.write(dict_news)
		await rw_json.stop()
