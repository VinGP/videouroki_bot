from SETTINGS import *
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "BOT TOKEN HERE"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dc = {
    "test_answer": "Тест: Образ «идеального города в классицистических ансамблях парижа и петербурга",
    "answers": {
        "Архитектор ансамбля\xa0площади Людовика XV\xa0(ныне —\xa0площадь Согласия;\xa01757-1779) в Париже\n": "Жак "
                                                                                                               "Анж "
                                                                                                               "Габриель",
        "Архитектор\xa0здания\xa0Адмиралтейства\xa0в Петербурге\n": "Андреян "
                                                                    "Дмитриевич "
                                                                    "Захаров",
        "Архитектор\xa0здания\xa0Академии наук в Петербурге\n": "Джакомо Кваренги",
        'Архитектор\xa0русского "екатерининского классицизма"\n': ["Джакомо Кваренги"],
        "Верно ли, что в архитектуре XVIII века были сделаны шаги по преодолению феодальной хаотичности"
        " городской застройки и созданию ансамблей, рассчитанных на свободный обзор.\n": "Да",
        "Как называется и где находится представленное в задании сооружение?\n\n": [
            "Адмиралтейство",
            "Санкт-Петербург",
        ],
        "Неоклассицизм в архитектуре характеризовался.....\n": "созданием "
                                                               "архитектурных "
                                                               "ансамблей, "
                                                               "рассчитанных на "
                                                               "свободный обзор",
        "Один из первых архитекторов неоклассицизма\n": "Жак Анж Габриель",
    }
}


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    res = "<i>" + dc["test_answer"] + "</i>" + "\n\n"
    # dc = {"Один из первых архитекторов неоклассицизма\n": "Жак Анж Габриель",}
    for k, i in dc['answers'].items():
        res += "<u><b>" + k.strip() + "</b></u>\n"
        res += "\n".join(i) + "\n\n" if type(i) == list else i + "\n\n"
    res.strip()
    await message.answer(res, parse_mode="html")


from test import get_test_answer


@dp.message_handler(commands=["fake"])
async def fake_url(message: types.Message):
    await message.answer(text=await get_test_answer(message.text.split()[-1]))


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    # from test import
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
