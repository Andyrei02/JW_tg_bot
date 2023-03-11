# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from utils.loader import dp


@dp.message_handler(CommandHelp())
async def help(message: types.Message):
	# Send a help message to the user
	await message.answer("Bun venit la botul JW_news! Iată comenzile disponibile:\n"
						 "\n"
						 "/start - Porniți botul\n"
						 "/help - Afișează acest mesaj de ajutor\n"
						 "/list_news - Afișează o listă a ultimelor știri"
						 "\n"
						 "Dacă aveți întrebări sau întâmpinați probleme, vă rugăm să nu ezitați să ne trimiteți un mesaj la @andyrei. Vă mulțumim că ați folosit botul nostru!")
