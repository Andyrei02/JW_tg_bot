# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from utils.loader import dp
from utils import config
from utils.users_database import UserDatabase
from handlers.keyboard import daily_news_keyboard


@dp.message_handler(CommandStart())
async def start(message: types.Message):
	keyboard = daily_news_keyboard()
	
	# Send a welcome message to the user
	await message.answer("Bine ați venit la JW_news!"
						 "Acest bot vă oferă cele mai recente actualizări de știri de la jw.org în fiecare zi, la ora 7:00 AM, și textul zilei la ora 8:00"
						 "Dacă întâmpinați probleme sau aveți sugestii, vă rugăm să nu ezitați să ne trimiteți un mesaj la @andyrei. Căutăm mereu să îmbunătățim botul nostru și salutăm feedback-ul tău."
						 "Vă mulțumim că folosiți botul nostru!", reply_markup=keyboard)


	await add_user(message)


async def add_user(message):
	db = UserDatabase(config.USER_DATABASE_PATH)
	await db.connect()

	# Add a user
	user = (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username) #types.User(id=1234567890, first_name='John', last_name='Doe', username='johndoe')
	await db.add_user(user)

	# Retrieve all users
	users = await db.get_all_users()

	# Close the database connection
	await db.close()
