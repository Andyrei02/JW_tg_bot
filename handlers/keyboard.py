from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from utils.loader import dp
from . import start, help_msg, daily_news, daily_text, list_news, recommendation, update, echo


def public_keyboard():
	# define the buttons
	daily_news_button = KeyboardButton(text='Noutatea recentă 🗞')
	daily_text_button = KeyboardButton(text='Textul zilei 📰')
	recommendation_button = KeyboardButton(text='Recomandări')
	update_button = KeyboardButton(text='actualizează datele 🔄')
	help_button = KeyboardButton(text="Ajutor")

	# define the keyboard
	inline_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	inline_kb.add(daily_news_button).insert(daily_text_button).add(recommendation_button).add(update_button).insert(help_button)
	return inline_kb


@dp.message_handler(state=None)
async def keyboard_handler(message: Message):
	try:
		if message.text == "/start":
			await start.start(message)
		elif message.text in ("Ajutor", "/help"):
			await help_msg.help_msg(message)
		elif message.text in ("Noutatea recentă 🗞", "/daily_news"):
			await daily_news.public_daily_news(message.chat.id)
		elif message.text in ("Textul zilei 📰", "/daily_text"):
			await daily_text.public_daily_text(message.chat.id)
		elif message.text in ("Recomandări", "/recommendation"):
			await recommendation.public_recommendation(message.chat.id)
		elif message.text in ("actualizează datele 🔄", "/update"):
			await update.update(message)
		else:
			await echo.echo(message)

	except Exception as e:
		print(e)
