# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.


import psycopg2

class UserDatabase:
	def __init__(self, db_config):
		self.db_config = db_config
		self.connection = None
		self.cursor = None
	
	async def connect(self):
		self.connection = psycopg2.connect(**self.db_config)
		self.cursor = self.connection.cursor()
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
			chat_id BIGINT PRIMARY KEY,
			first_name VARCHAR(255),
			last_name VARCHAR(255),
			username VARCHAR(255),
			language VARCHAR(255) DEFAULT NULL,
			news_time VARCHAR(255) DEFAULT NULL,
			poem_time VARCHAR(255) DEFAULT NULL
		)''')

	async def add_user(self, user):
		try:
			self.cursor.execute("INSERT INTO users (chat_id, first_name, last_name, username, language, news_time, poem_time) VALUES (%s, %s, %s, %s, %s, %s, %s)", (
				user[0],
				user[1],
				user[2] or '',
				user[3] or '',
				user[4] or '',
				user[5] or '',
				user[6] or ''
			))
			self.connection.commit()
		except psycopg2.errors.UniqueViolation:
			# User already exists in database
			pass

	async def get_user(self, chat_id):
		self.cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
		result = self.cursor.fetchone()
		if result:
			return {
				'chat_id': result[0],
				'first_name': result[1],
				'last_name': result[2] or None,
				'username': result[3] or None,
				'language': result[4] or None,
				'news_time': result[5] or None,
				'poem_time': result[6] or None
			}

	async def get_all_users(self):
		self.cursor.execute("SELECT * FROM users")
		results = self.cursor.fetchall()
		return [{
			'chat_id': result[0],
			'first_name': result[1],
			'last_name': result[2] or None,
			'username': result[3] or None,
			'language': result[4] or None,
			'news_time': result[5] or None,
			'poem_time': result[6] or None
		} for result in results]

	async def close(self):
		self.connection.close()
