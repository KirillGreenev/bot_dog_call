import random
import requests
import telebot
from telebot import types
from config import BOT_TOKEN
from parser_group import get_members_group
from multiprocessing import Process, Queue
from repository import create_connection,create_table, select_all_prediction, close_connection

sql_create_prediction_table = """
        CREATE TABLE IF NOT EXISTS prediction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        );
        """

bot = telebot.TeleBot(BOT_TOKEN)
conn = create_connection("mydatabase.db")
create_table(conn, sql_create_prediction_table)



@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')


@bot.message_handler(commands=['созыв', 'all'])
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

@bot.message_handler(commands=['pr','судьба', 'предсказание'])
def get_prediction(message):
    if conn is not None:
        r = select_all_prediction(conn)
        if len(r) == 0:
            bot.send_message(message.chat.id, "В данный момент предсказаний нету, но мы их обязательно добавим")
        else:
            ms = random.choice(r)
            name = '@' + message.from_user.username if message.from_user.username else message.from_user.first_name
            bot.send_message(message.chat.id, f"🔮")
            bot.send_message(message.chat.id, f"Предсказание для {name}:\n{ms}")
    else:
        bot.send_message(message.chat.id, "Упс что-то пошло не так, но мы это обязательно исправим")


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
        close_connection(conn)
    except Exception as e:
        print(f"Ошибка в боте: {e}")
