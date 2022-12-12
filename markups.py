from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

all_usr = InlineKeyboardButton("Всего юзеров", callback_data="all_usr")
send_all = InlineKeyboardButton("Рассылка", callback_data="send_all")
admin_m = InlineKeyboardMarkup().add(all_usr).add(send_all)

otmena = InlineKeyboardButton("Отмена", callback_data="otmena")
otmena_m = InlineKeyboardMarkup().add(otmena)

lich_cab = InlineKeyboardButton("Войти", callback_data="Login")
start_m = InlineKeyboardMarkup().add(lich_cab)


bron = InlineKeyboardButton("Забронировать", callback_data="bron")
my_bron = InlineKeyboardButton("Мои бронирования", callback_data="my_bron")
main_m = InlineKeyboardMarkup().add(bron).add(my_bron)


passw = InlineKeyboardButton("Ввести пароль:", callback_data="log_in")
login = InlineKeyboardMarkup().add(passw)
