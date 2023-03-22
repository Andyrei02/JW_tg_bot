# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from aiogram import types
from aiogram.dispatcher.filters import Command

from utils.loader import dp
from utils.users_database import UserDatabase
from utils import config

from utils import update_data


@dp.message_handler(Command("update"))
async def update(message: types.Message):

	# message 2
	with open('media/loading.gif', 'rb') as gif:
		update_message = await dp.bot.send_animation(chat_id=message.chat.id, animation=gif)
	# update
	await update_data.update_data()
	# delete message 1 and 2
	await update_message.delete()

	# message 3
	with open("media/complete.png", "rb") as photo:
		await dp.bot.send_photo(message.chat.id, caption="Datele au fost actualizate", photo=photo)

	await message.delete()