# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from utils.loader import dp


async def help_msg(message):
	await message.answer("Bun venit la botul JW_news! Iată comenzile disponibile:\n"
						 "\n"
						 "/start - Porniți botul\n"
						 "/help - Afișează acest mesaj de ajutor\n"
						 "/list_news - Afișează o listă a ultimelor știri\n"
						 "/daily_news - Afișează o știre pe ziua de azi\n"
						 "/daily_text - Afișează textul zilei de azi\n"
						 "\n"
						 "Dacă aveți întrebări sau întâmpinați probleme, vă rugăm să nu ezitați să ne trimiteți un mesaj la @andyrei. Vă mulțumim că ați folosit botul nostru!")
