from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton("Количество репорта"))
main_keyboard.add(KeyboardButton("Очистить репорт"))

confirm_clear_keyboard = InlineKeyboardMarkup()
confirm_clear_keyboard.add(
    InlineKeyboardButton("Да", callback_data="clear_reports_yes"),
    InlineKeyboardButton("Нет", callback_data="clear_reports_no")
)