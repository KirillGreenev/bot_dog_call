import time
import random
import requests
import telebot
from telebot import types
from config import BOT_TOKEN
from parser_group import get_members_group
from multiprocessing import Process, Queue
from repository import (create_connection, create_table,
                        select_all_prediction, close_connection,
                        insert_table, update_prediction, delite_prediction)

sql_create_prediction_table = """
        CREATE TABLE IF NOT EXISTS prediction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        );
        """

bot = telebot.TeleBot(BOT_TOKEN)
conn = create_connection("mydatabase.db")
create_table(conn, sql_create_prediction_table)

# Хранение состояния
user_states = {}
update_id_prediction = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')

@bot.message_handler(commands=['add'])
def add_prediction_handler(message):
    user_states[message.from_user.id] = 'waiting_for_add'
    bot.send_message(message.chat.id, "Напиши предсказание, которое хочешь добавить")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_add')
def ask_text_add(message):
    text = message.text
    last_id = insert_table(conn, "INSERT INTO prediction(text) VALUES(?)", (text,))
    if last_id is not None:
        bot.send_message(message.chat.id, f"Предсказание успешно добавлено. Id для удаления или изменения {last_id}")
    else:
        bot.send_message(message.chat.id, "Не удалось добавить предсказание")
    del user_states[message.from_user.id]  # Удаляем состояние после завершения


@bot.message_handler(commands=['upd'])
def update_prediction_handler(message):
    user_states[message.from_user.id] = 'waiting_for_id_update'
    bot.send_message(message.chat.id, "Напиши id предсказания, которое хотите изменить")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_id_update')
def ask_id_update(message):
    try:
        id = int(message.text)
        user_states[message.from_user.id] = 'waiting_for_text_update'
        update_id_prediction[message.from_user.id] = id
        bot.send_message(message.chat.id, "Введите текст на который хотите заменить текущее предсказание")
    except ValueError:
        bot.send_message(message.chat.id, "id должно быть числом")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_text_update')
def ask_text_update(message):
    id = update_id_prediction[message.from_user.id]
    text = message.text

    if update_prediction(conn, id, text):
        bot.send_message(message.chat.id, "Предсказание успешно изменено")
    else:
        bot.send_message(message.chat.id, "Не удалось  изменить предсказание")

    del user_states[message.from_user.id]
    del update_id_prediction[message.from_user.id]


@bot.message_handler(commands=['del'])
def delite_prediction_handler(message):
    user_states[message.from_user.id] = 'waiting_for_id_delite'
    bot.send_message(message.chat.id, "Напиши id предсказания, которое хотите удалить")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_id_delite')
def ask_id_delite(message):
    try:
        id = int(message.text)
        if delite_prediction(conn, id):
            bot.send_message(message.chat.id, "Предсказание успешно удалено")
        else:
            bot.send_message(message.chat.id, "Не удалось удалить предсказание")

        del user_states[message.from_user.id]
    except ValueError:
        bot.send_message(message.chat.id, "id должно быть числом")


@bot.message_handler(commands=['созыв', 'all', 'call'])
def dog_call(message):
    try:
        q = Queue()
        new_process = Process(target=get_members_group, args=(message.chat.id, q), daemon=True)
        new_process.start()
        members_group = q.get(timeout=4)
        new_process.join()
    except:
        members_group = 'Приглашаем всех участников группы!'
    bot.send_message(message.chat.id,
                     f"Собачий созыв!! АУУУУУУ🐺🌙\n{members_group}\nпоставьте реакцию дизлайка, если вы не придете в созвон, это важно")


@bot.message_handler(commands=['котэ', 'cat'])
def get_cat(message):
    respons = requests.get('https://api.thecatapi.com/v1/images/search')
    if respons.status_code == 200:
        bot.send_photo(message.chat.id, respons.json()[0]["url"])
    else:
        bot.send_message(message.chat.id, 'Здесь должна была быть картинка с котиком :(')


@bot.message_handler(commands=['pr', 'судьба', 'предсказание'])
def get_prediction(message):
    if conn is not None:
        r = select_all_prediction(conn)
        if len(r) == 0:
            bot.send_message(message.chat.id, "В данный момент предсказаний нету, их можно добавить через команду /menu")
        else:
            random.seed(time.time())
            ms = random.choice(r)
            name = '@' + message.from_user.username if message.from_user.username else message.from_user.first_name
            bot.send_message(message.chat.id, "🔮")
            bot.send_message(message.chat.id, f"Предсказание для {name}:\n{ms}")
    else:
        bot.send_message(message.chat.id, "Упс что-то пошло не так, но мы это обязательно исправим")

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Добавить")
    button2 = types.KeyboardButton("Изменить")
    button3 = types.KeyboardButton("Удалить")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Добавить":
        add_prediction_handler(message)
    elif message.text == "Изменить":
        update_prediction_handler(message)
    elif message.text == "Удалить":
        delite_prediction_handler(message)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка в боте: {e}")
    finally:
        close_connection(conn)
