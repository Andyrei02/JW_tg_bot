# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types

from utils.loader import dp


@dp.message_handler(state=None)
async def message(message: types.Message):
	# Echo the user's message back to them
	await message.answer(message.text)
