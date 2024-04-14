from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from parser_grup import get_members_grup
from config import BOT_TOKEN, GROUP_ID
import requests

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(f'Привет {message.from_user.first_name}!')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь'

    )


# Команда /созыв
@dp.message(Command(commands=['созыв']))
async def summon_all(message: Message):
    await message.answer(
        f"Собачий созыв!! АУУУУУУ🐺🌙\n{member_grup}\nпоставьте реакцию дизлайка, если вы не придете в созвон, это важно")


# Команда /котэ
@dp.message(Command(commands=['котэ']))
async def get_cat(message: Message):
    respons = requests.get('https://api.thecatapi.com/v1/images/search')
    if respons.status_code == 200:
        await message.answer_photo(respons.json()[0]["url"])
    else:
        await message.answer('Здесь должна была быть картинка с котиком :(')


if __name__ == '__main__':
    try:
        member_grup = get_members_grup(GROUP_ID)
        dp.run_polling(bot)
    except:
        print("Ничего не работает")
