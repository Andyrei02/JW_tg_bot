# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import os
import asyncio
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import TelegramAPIError

from utils.loader import dp
from utils import config
from handlers.keyboard import admin_inline_keyboard


@dp.message_handler(Command("admin"))
async def message(message: types.Message):
	if str(message.from_user.id) == str(config.ADMIN_ID):
		await admin_panel(message)


async def admin_panel(message):
	inline_kb = admin_inline_keyboard()
	await message.answer("Hello admin", reply_markup=inline_kb)


@dp.callback_query_handler(text='/upload')
async def upload_callback_handler(query: types.CallbackQuery):
	if str(query.from_user.id) == str(config.ADMIN_ID):
		await upload_db(query.message)


@dp.callback_query_handler(text='/download')
async def upload_callback_handler(query: types.CallbackQuery):
	if str(query.from_user.id) == str(config.ADMIN_ID):
		await download_db(query.message)


async def upload_db(message: types.Message):
	upload_message = await message.answer("Please upload the file you want to send to the bot.")
	
	# Wait for the user to upload a file
	@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
	async def wait_file(message: types.Message):
		file_id = message.document.file_id
		file = await dp.bot.get_file(file_id)
		local_file_path = "data/users_data.db"
		await dp.bot.download_file(file.file_path, local_file_path)

		# Process the uploaded file here
		await message.answer("File received. Thank you!")
		
	# Set a timeout for the file upload
	await asyncio.sleep(300)  # Wait 5 minutes
	await message.answer("Sorry, time is up. Please try again.")


async def download_db(message: types.Message):
	with open("data/users_data.db", "rb") as file:
		try:
			await dp.bot.send_document(chat_id=config.ADMIN_ID, document=file)
		except TelegramAPIError as e:
			await message.answer(f"Failed to send the file. Error: {e}")
	await message.delete()
