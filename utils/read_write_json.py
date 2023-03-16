# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.

import json
import asyncio

class ReadWriteJson:
	def __init__(self, file_path):
		self.file_path = file_path
		self.queue = asyncio.Queue()

	async def _write(self):
		with open(self.file_path, 'w') as f:
			while True:
				data = await self.queue.get()
				if data is None:
					break
				json.dump(data, f, indent=4)
				f.write('\n')
				f.flush()

	async def start(self):
		self.task = asyncio.create_task(self._write())

	async def stop(self):
		await self.queue.put(None)
		await self.task

	async def write(self, data):
		await self.queue.put(data)

	async def read(self):
		with open(self.file_path, 'r') as f:
			return json.load(f)
