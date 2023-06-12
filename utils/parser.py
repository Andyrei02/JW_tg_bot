# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import asyncio
import aiohttp
import datetime
import requests
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class NewsScraper:
	def __init__(self, source_link, news_link):
		self.source_link = source_link
		self.news_link = news_link

	async def get_site_page(self, link):
		async with aiohttp.ClientSession() as session:
			async with session.get(link) as resp:
				response =  await resp.text()
		return BeautifulSoup(response, 'lxml')

	async def get_last_news_block(self, soup):
		block = soup.find(class_="landingPagePrimaryFeature")
		block = block.find(class_="presentationIntent-desktop")
		return block

	async def get_img(self, block):
		img_block = block.find(class_="syn-img pnr")
		return img_block.find("img")["src"]

	async def get_title(self, block):
		title_block = block.find(class_="syn-body pnr")
		title = title_block.find("h3").text
		return title

	async def get_url(self, block):
		url_block = block.find(class_="syn-body pnr")
		url = self.source_link + url_block.find("a")["href"]
		return url

	async def get_introduction(self, url):
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				response =  await resp.text()

		content_page = BeautifulSoup(response, 'lxml')
		content_block = content_page.find(class_="contentBody")
		pGroup = content_block.find(class_="pGroup")
		intro = "\n" + content_block.find(class_="p2").text

		return intro

	async def get_dict_news(self):
		soup = await self.get_site_page(self.news_link)
		block = await self.get_last_news_block(soup)
		img = await self.get_img(block)
		title = await self.get_title(block)
		url = await self.get_url(block)
		intro = await self.get_introduction(url)

		return {"img": img, "title": title.strip(), "intro": intro, "url": url}

	async def get_news(self):
		return await self.get_dict_news()


class DailyTextScraper:
	def __init__(self, source_link, url):
		self.source_link = source_link
		self.url = url + self.get_today_date()

	async def get_site_page(self):
		response = requests.get(self.url)
		return BeautifulSoup(response.text, "lxml")

	def get_today_date(self):
		today = datetime.date.today()
		return today.strftime('%Y/%-m/%-d')

	def format_verse(self, daily_text):
		verse_soup = daily_text[0].p
		text = verse_soup.em.text.strip()
		link = self.source_link + verse_soup.a['href']
		reference = verse_soup.a.em.text.strip()

		return f'{text} <a href="{link}">{reference}</a>)'

	def format_body(self, daily_text):
		body_soup = daily_text[0].find("div", {"class": "bodyTxt"}).p

		body = body_soup.get_text()
		links = []
		for a in body_soup.find_all('a'):
			link_text = a.get_text()
			link_url = a['href']
			link = f'<a href="{self.source_link}{link_url}">{link_text}</a>'
			links.append(link)

		return body + "\n" + '\n'.join(links)

	async def get_daily_text(self):
		soup = await self.get_site_page()
		content = soup.find("div", {"id": "dailyText"})
		daily_text = content.select('.tabContent:nth-of-type(2)')

		title = daily_text[0].header.text.strip()
		verse = self.format_verse(daily_text)
		body = self.format_body(daily_text)

		return {"title": title, "verse": verse, "body": body}


class ListNewsScraper:
	def __init__(self, url):
		self.url = url

	async def scrape(self):
		xml_data = urlopen(self.url).read()
		root = ET.fromstring(xml_data)
		news_list = []
		for item in root.iter("item"):
			title = item.find("title").text
			link = item.find("link").text
			date_str = item.find("pubDate").text
			romanian_date = await self._convert_date_to_romanian(date_str)
			news_list.append({"title": title, "link": link, "date": romanian_date})
		return news_list[::-1]

	async def _convert_date_to_romanian(self, date_str):
		date = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
		months = [
			'ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie',
			'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie'
		]
		romanian_date_str = f"{date.day} {months[date.month - 1]} {date.year}"
		return romanian_date_str


class RecommendationScraper:
	def __init__(self, source_url, url):
		self.source_url = source_url
		self.url = url

	async def get_site_page(self):
		async with aiohttp.ClientSession() as session:
			async with session.get(self.url) as resp:
				response =  await resp.text()
		return BeautifulSoup(response, 'lxml')

	async def scrape(self):
		soup = await self.get_site_page()
		content_block = soup.find("main", {"id": "content"})
		container = content_block.find("div", {"class": "sectionSynopsis"})
		content = container.find("div", {"class": "sect-syn-content"})
		list_items = content.find_all("div", {"class": "synopsis"})
		return list_items

	async def extract_recommendation(self, item):
		soup = item.find("div", {"class": "syn-body lss"})
		body_title = soup.find("h3")
		body_link = soup.find("a")["href"]
		body_img = item.find("div", {"class": "syn-img lss"})
		title = body_title.text.strip()
		link = self.source_url + body_link
		img = body_img.find("img")["src"]
		return {"title": title, "link": link, "img": img}

	async def get_recommendations(self):
		list_items = await self.scrape()
		recommendation_list = []
		for item in reversed(list_items):
			recommendation = await self.extract_recommendation(item)
			recommendation_list.append(recommendation)
		return recommendation_list
