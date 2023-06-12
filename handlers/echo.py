# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

async def echo(message):
	# Echo the user's message back to them
	await message.answer(message.text)
