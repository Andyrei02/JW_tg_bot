# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from utils.loader import db
from handlers import keyboard


async def start(message):
	
	# Send a welcome message to the user
	await message.answer("Bine ați venit la JW_news! "
						 "\nAcest bot vă oferă cele mai recente actualizări de știri de la jw.org în fiecare zi, la ora 7:00 AM, și textul zilei la ora 8:00"
						 "\nDacă întâmpinați probleme sau aveți sugestii, vă rugăm să nu ezitați să ne trimiteți un mesaj la @andyrei. Căutăm mereu să îmbunătățim botul nostru și salutăm feedback-ul tău."
						 "\n❗❗❗\nBotul în nici un caz nu este menit sa înlocuiască siteul jw.org\n❗❗❗"
						 "\nVă mulțumim că folosiți botul nostru!", reply_markup=keyboard.public_keyboard())

	await add_user(message)


async def add_user(message):
	await db.connect()

	# Add a user
	user = (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, '', '', '')
	await db.add_user(user)

	# Close the database connection
	await db.close()
