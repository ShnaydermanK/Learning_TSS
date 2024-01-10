import asyncio

from aiogram import Bot, Dispatcher, types
from datetime import datetime

from aiogram.enums import ParseMode

from config import config
from Sql import Request
from middlewares import DBSession
from pool import create_database_pools
from aiogram import F
from aiogram.utils import markdown
from html import escape
from stop_slova import stop_slova

async def main() -> None:
    TOKEN_BOT = config.tg_bot.token
    print(TOKEN_BOT)

    # Создание пула подключений к базе данных
    creat_pool = await create_database_pools()

    # Инициализация бота и диспетчера
    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher()
    dp.update.middleware.register(DBSession(creat_pool))

    # Обработчик добавления нового участника в группу
    @dp.message(F.new_chat_members)
    async def handle_new_chat_member(message: types.Message, request: Request):
        await request.create_table()

        chat_id = message.chat.id
        chat_name = message.chat.title
        user_id = message.from_user.id
        username = message.from_user.username
        mess = message.text
        date = datetime.now()

        if message.new_chat_members:
            for member in message.new_chat_members:
                escaped_first_name = escape(member.first_name, quote=False)
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"""Привет, {escaped_first_name}!\n\n"""
                         "Напиши своё Имя и номер телефона.",
                    parse_mode=ParseMode.HTML,
                )

        print(chat_name, mess)

        await request.insert_history(chat_id, chat_name, user_id, username,mess, date, "joined")



    # Обработчик удаления участника из группы
    @dp.message(F.left_chat_member)
    async def handle_left_chat_member(message: types.Message, request: Request):
        await request.create_table()

        chat_id = message.chat.id
        chat_name = message.chat.title
        user_id = message.from_user.id
        username = message.from_user.username
        mess = message.text
        date = datetime.now()

        print(chat_name)

        await request.insert_history(chat_id, chat_name, user_id, username, mess, date, "left")

        target_user_ids = [330823635, 394820351, 626319958]  # Замените этот ID на фактический ID пользователя

        for target_user_id in target_user_ids:

        # Отправляем личное сообщение
            await bot.send_message(target_user_id,f"Участник <b>{username}</b> в группе <b>{chat_name}</b> покинул группу.", parse_mode='HTML')

        # Обработчик текстовых сообщений

    @dp.message(lambda message: message.text and not message.text.startswith('/'))
    async def handle_message(message: types.Message, request: Request):
        await request.creat_table_history()
        await request.creat_table_stop_slova()
        chat_id = message.chat.id
        chat_name = message.chat.title
        user_id = message.from_user.id
        username = message.from_user.username
        text = message.text
        date = datetime.now()

        print(chat_name)

        await request.insert_table_history(chat_id, chat_name, user_id, username, date, text)

        if any(stop_word in text.split() for stop_word in stop_slova):
            print(f"Какой то хулиган {username} в группе {chat_name} написал плохое слово: {text}")
            for stop_word in stop_slova:
                if stop_word in text:
                    print(f"Стоп слово: {stop_word}")
                    break



            # Получаем id пользователя, которому нужно отправить личное сообщение
            target_user_ids = [330823635, 394820351, 626319958]  # Замените этот ID на фактический ID пользователя

            for target_user_id in target_user_ids:

                # Отправляем личное сообщение
                await bot.send_message(target_user_id, f"Какой то хулиган <b>{username}</b> в группе <b>{chat_name}</b> написал плохое слово: {text}", parse_mode='HTML')

                await request.insert_table_stop_slova(chat_id, chat_name, user_id, username, date, text)


    # Удаление вебхука и запуск опроса бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
