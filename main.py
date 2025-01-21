import requests
import telebot
from config import BOT_TOKEN
from parser_grup import get_members_grup
from multiprocessing import Process, Queue

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')


@bot.message_handler(commands=['созыв'])
def dog_call(message):
    try:
        q = Queue()
        p1 = Process(target=get_members_grup, args=(message.chat.id, q), daemon=True)
        p1.start()
        members_grup = q.get(timeout=4)
        p1.join()
    except:
        members_grup = '/all'
    bot.send_message(message.chat.id,
                     f"Собачий созыв!! АУУУУУУ🐺🌙\n{members_grup}\nпоставьте реакцию дизлайка, если вы не придете в созвон, это важно")


@bot.message_handler(commands=['котэ'])
def get_cat(message):
    respons = requests.get('https://api.thecatapi.com/v1/images/search')
    if respons.status_code == 200:
        bot.send_photo(message.chat.id, respons.json()[0]["url"])
    else:
        bot.send_message(message.chat.id, 'Здесь должна была быть картинка с котиком :(')


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка в боте: {e}")
