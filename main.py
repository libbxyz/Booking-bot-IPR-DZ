import sqlite3

from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from db import Database
import markups as nav

bot = Bot(token="5849680317:AAEoD7tYg_v_dttyg4tKAW60aV4DMiTNkqQ")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

db = Database("database.db")


class admad(StatesGroup):
    ad = State()


class login_start(StatesGroup):
    logg = State()
    passw = State()


class log(StatesGroup):
    log = State()
    pasw = State()


class bronning(StatesGroup):
    text = State()


with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id):
            await message.answer('Здравствуйте!', reply_markup=nav.start_m)
        else:
            db.add_user(message.from_user.id, message.from_user.username)
            await bot.send_message(message.from_user.id, f"Добро пожаловать!\nЗарегистрируйтесь\nПридумайте логин:")
            await login_start.logg.set()
    else:
        await message.answer("Напиши мне в личку.")


@dp.message_handler(state=login_start.logg)
async def login_startt(message: types.Message, state: FSMContext):
    log = message.text
    await state.update_data(logg=log)
    await state.finish()
    await message.answer(str(db.start_log(message.from_user.id, log)))
    await login_start.passw.set()


@dp.message_handler(state=login_start.passw)
async def login_st_passw(message: types.Message, state: FSMContext):
    passw = message.text
    await state.update_data(passw=passw)
    await state.finish()
    await message.answer(str(db.start_log_passw(message.from_user.id, passw=passw)), reply_markup=nav.start_m)


@dp.callback_query_handler(text="all_usr")
async def all_usr(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Всего юзеров :  {db.all_usr()}", reply_markup=nav.admin_m)


@dp.callback_query_handler(text="send_all")
async def send_all(callback: types.CallbackQuery):
    await callback.message.answer("Введи текст объявления:", reply_markup=nav.otmena_m)
    await admad.ad.set()


@dp.message_handler(state=admad.ad)
async def getcount(message: types.Message, state: FSMContext):
    ad = message.text
    await state.update_data(ad=ad)
    await state.finish()
    cursor.execute("SELECT user_id FROM users")
    userbase = []
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        userbase.append(row)
    if len(userbase) > 1:
        for z in range(len(userbase)):
            await bot.send_message(userbase[z][0], text=f"‼️\n{ad}")
    else:
        await bot.send_message(userbase, f"‼️\n{ad}")
    await bot.send_message(message.from_user.id, text='Готово', reply_markup=nav.admin_m)


@dp.callback_query_handler(text="otmena", state=admad.ad)
async def otmena(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(ad="")
    await state.finish()
    await callback.message.delete()


@dp.callback_query_handler(text="Login")
async def Login(callback: types.CallbackQuery):
    await callback.message.answer("Введите логин:")
    await log.log.set()


@dp.message_handler(state=log.log)
async def login(message: types.Message, state: FSMContext):
    login_l = message.text
    await state.update_data(log=login_l)
    await state.finish()

    await message.answer(f"{db.check_log(message.from_user.id, login_l)}", reply_markup=nav.login)


@dp.callback_query_handler(text="log_in")
async def Log_in(callback: types.CallbackQuery):
    await callback.message.edit_text("Введите пароль:")
    await log.pasw.set()


@dp.message_handler(state=log.pasw)
async def passw(message: types.Message, state: FSMContext):
    login_p = message.text
    await state.update_data(pasw=login_p)
    await state.finish()
    await message.answer(f"{db.check_passw(message.from_user.id, login_p)}", reply_markup=nav.main_m)


@dp.callback_query_handler(text="bron")
async def bron(callback: types.CallbackQuery):
    await callback.message.answer(
        "Введите дату, время приезда, номер комнаты, номер телефона\n\nПример:\n12.08.2023\n21:00\n198\n+79639877678")
    await bronning.text.set()


@dp.message_handler(state=bronning.text)
async def bronned(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await state.finish()

    await message.answer(str(db.new_bron(message.from_user.id, text)))


@dp.callback_query_handler(text="my_bron")
async def my_bron(callback: types.CallbackQuery):
    await callback.message.answer(f"Ваше бронирование:\n\n{str(db.check_bron(callback.from_user.id))}", reply_markup=nav.main_m)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
