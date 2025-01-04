import pymysql
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DATABASE, ADMINS
from keyboards import main_keyboard, confirm_clear_keyboard

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def connect_to_database():
    return pymysql.connect(
        host=DATABASE["host"],
        user=DATABASE["user"],
        password=DATABASE["password"],
        database=DATABASE["database"]
    )

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer(
            "Здравствуйте, администратор! Используйте клавиатуру для навигации по боту.",
            reply_markup=main_keyboard
        )
    else:
        await message.answer("У Вас нет доступа к этому боту.")

@dp.message_handler(lambda message: message.text == "Количество репорта")
async def report_count(message: types.Message):
    if message.from_user.id in ADMINS:
        connection = connect_to_database()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM reports WHERE active = 1")
            count = cursor.fetchone()[0]
        connection.close()
        await message.answer(f"В данный момент неотвеченных репортов: {count}")

@dp.message_handler(lambda message: message.text == "Очистить репорт")
async def clear_reports(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer(
            "Подтвердите очистку неотвеченных репортов.",
            reply_markup=confirm_clear_keyboard
        )

@dp.callback_query_handler(lambda callback: callback.data in ["clear_reports_yes", "clear_reports_no"])
async def confirm_clear(callback: types.CallbackQuery):
    if callback.from_user.id in ADMINS:
        if callback.data == "clear_reports_yes":
            connection = connect_to_database()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM reports WHERE active = 1")
                connection.commit()
            connection.close()
            await callback.message.answer("Все неотвеченные репорты очищены.")
        else:
            await callback.message.answer("Очистка отменена.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)