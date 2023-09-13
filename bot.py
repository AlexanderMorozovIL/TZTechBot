from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd
import sqlite3


TOKEN = '6482513022:AAHO7OjWudrGK9v7JUVlFtbNsqYZNJ5oLJU'

conn = sqlite3.connect('sites.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sites
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                xpath TEXT NOT NULL)''')
conn.commit()
c.close()
conn.close()


def start(update, context):
    """Обработчик команды '/start' для запуска бота."""

    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text=(
            f'Привет, {name}! Я бот для загрузки файлов. '
            f'Пришли мне файл в формате таблицы Excel '
            f'с полями title, url и xpath.')
        )


def upload_file(update, context):
    """
    Обработчик для загрузки файла с данными,
    парсинга его содержимого и сохранения в базу данных.
    """
    chat = update.effective_chat
    file = context.bot.getFile(update.message.document.file_id)
    file.download('data.xlsx')
    df = pd.read_excel('data.xlsx')

    conn = sqlite3.connect('sites.db')
    c = conn.cursor()

    for index, row in df.iterrows():
        title = row['title']
        url = row['url']
        xpath = row['xpath']

        c.execute(
            'INSERT INTO sites (title, url, xpath) VALUES (?, ?, ?)',
            (title, url, xpath)
        )
        conn.commit()

    c.close()
    conn.close()

    text = (
        f'Название сайта: {title}\n'
        f'Ссылка на сайт: {url}\n'
        f'Путь к элементу: {xpath}'
        )
    context.bot.send_message(
        chat_id=chat.id,
        text=text
    )


def main():
    """
    Основная функция для запуска Telegram бота.

    Создает экземпляр бота, настраивает обновления,
    добавляет обработчики команды '/start'
    и загрузки документов, начинает опрос обновлений и
    ожидает завершения работы бота.
    """

    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.document, upload_file))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
