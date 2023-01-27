from config import *
import logging
from aiogram import Bot, Dispatcher, executor, types
from get_answer_async import get_test_answer
from message_texts import *

API_TOKEN = "BOT TOKEN HERE"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs.log",
)
logger = logging.getLogger(__name__)


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
        except Exception as err:
            logger.exception(err)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
        ]
    )


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer(GREETINGS, parse_mode="html")


@dp.message_handler(commands=["logs"])
async def get_logs(message: types.Message):
    print(ADMINS)
    print(message.from_user.id)
    if message.from_user.id in ADMINS:
        await bot.send_document(
            chat_id=message.chat.id, document=open("logs.log", "rb")
        )
    else:
        await echo(message)


@dp.message_handler(commands=["fake"])
async def fake_url(message: types.Message):
    answers = await get_test_answer(message.text.split()[-1])
    res = "<i>" + answers["test_title"] + "</i>" + "\n\n"
    for k, i in answers["answers"].items():
        res += "<u><b>" + k.strip() + "</b></u>\n"
        res += "\n".join(i) + "\n\n" if type(i) == list else i + "\n\n"
    res += f"Текстовая версия теста: {answers['test_page_url']}"
    await message.answer(res, parse_mode="html")


@dp.message_handler()
async def echo(message: types.Message):
    logger.info(
        f"Новое сообщение {message.text} от {message.from_user.id=} {message.from_user.url=}"
    )
    if "videouroki.net/tests/" in message.text:
        a = await message.answer("Запрос обрабатывается, подождите...")
        try:
            answers = await get_test_answer(message.text.split()[-1])
            res = "<i>" + answers["test_title"] + "</i>" + "\n\n"
            for k, i in answers["answers"].items():
                res += "<u><b>" + k.strip() + "</b></u>\n"
                res += "\n".join(i) + "\n\n" if type(i) == list else i + "\n\n"
            res += f"Текстовая версия теста: {answers['test_page_url']}"
            await message.reply(res, parse_mode="html")
        except Exception as e:
            logger.error(e, exc_info=True)
            await message.answer(
                "Вовремя прохождения теста произошла ошибка. Попробуйте позже"
            )
        await a.delete()
    else:
        await message.answer("Я не знаю, что на это ответить")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
