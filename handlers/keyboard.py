from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def daily_news_keyboard():
	# define the buttons
	daily_news_button = KeyboardButton(text='/daily_news')
	daily_text_button = KeyboardButton(text='/daily_text')
	update_button = KeyboardButton(text='/update')

	# define the keyboard
	inline_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	inline_kb.add(daily_news_button).insert(daily_text_button).add(update_button)
	return inline_kb


def admin_inline_keyboard():
	upload = InlineKeyboardButton(text='/upload', callback_data='/upload')
	download = InlineKeyboardButton(text='/download', callback_data='/download')

	# Create the keyboard
	admin_kb = InlineKeyboardMarkup().add(upload, download)
	return admin_kb
