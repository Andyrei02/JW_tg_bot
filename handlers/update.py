# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

from utils.loader import dp

from utils import update_data


async def update(message):

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
