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
	await message.answer("Here's some help:\n\n"
						 "/start - Start the bot\n"
						 "/help - Show this help message")
