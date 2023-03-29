# Copyright (c) 2023 Andrei Cenușă
# All rights reserved.
#
# This code is licensed under the MIT License.
# See LICENSE for details.


import mysql.connector


class UserDatabase:
	def __init__(self, db_config):
		self.db_config = db_config
		self.connection = None
		self.cursor = None

	async def connect(self):
		self.connection = mysql.connector.connect(**self.db_config)
		self.cursor = self.connection.cursor()
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
			chat_id INT PRIMARY KEY,
			first_name VARCHAR(255),
			last_name VARCHAR(255),
			username VARCHAR(255)
		)''')

	async def add_user(self, user):
		try:
			self.cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (
				user[0],
				user[1],
				user[2] or '',
				user[3] or ''
			))
			self.connection.commit()
		except mysql.connector.errors.IntegrityError:
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
				'username': result[3] or None
			}

	async def get_all_users(self):
		self.cursor.execute("SELECT * FROM users")
		results = self.cursor.fetchall()
		return [{
			'chat_id': result[0],
			'first_name': result[1],
			'last_name': result[2] or None,
			'username': result[3] or None
		} for result in results]

	async def close(self):
		self.connection.close()












# import sqlite3


# class UserDatabase:
# 	def __init__(self, db_file):
# 		self.db_file = db_file
# 		self.connection = None
# 		self.cursor = None

# 	async def connect(self):
# 		self.connection = sqlite3.connect(self.db_file)
# 		self.cursor = self.connection.cursor()
# 		self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
# 			chat_id INTEGER PRIMARY KEY,
# 			first_name TEXT,
# 			last_name TEXT,
# 			username TEXT
# 		)''')

# 	async def add_user(self, user):
# 		try:
# 			self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (
# 				user[0],
# 				user[1],
# 				user[2] or '',
# 				user[3] or ''
# 			))
# 			self.connection.commit()
# 		except sqlite3.IntegrityError:
# 			# User already exists in database
# 			pass

# 	async def get_user(self, chat_id):
# 		self.cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
# 		result = self.cursor.fetchone()
# 		if result:
# 			return {
# 				'chat_id': result[0],
# 				'first_name': result[1],
# 				'last_name': result[2] or None,
# 				'username': result[3] or None
# 			}

# 	async def get_all_users(self):
# 		self.cursor.execute("SELECT * FROM users")
# 		results = self.cursor.fetchall()
# 		return [{
# 			'chat_id': result[0],
# 			'first_name': result[1],
# 			'last_name': result[2] or None,
# 			'username': result[3] or None
# 		} for result in results]

# 	async def close(self):
# 		self.connection.close()
