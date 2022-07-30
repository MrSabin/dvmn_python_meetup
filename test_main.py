import datetime
import locale
import os
import sqlite3

import telegram
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, update
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Updater)
from utils import db_to_json

# locale.setlocale(locale.LC_ALL, "ru")
bot_db_speaker = [(1, 'партнер, Data Insight, Вице-президент IBF', 
                   'Фёдор Федоров', 'Вступительные мероприятия', None, 
                   '171951902'), 
                   (2, 'заместитель генерального директора, FMNT', 'Денис Денисов', 
                   'Вступительные мероприятия', None, '171951902'), 
                   (3, 'Главный консультант, Россия Вперед', 'Борис Борисов', 
                   'Вступительные мероприятия', None, '171951902')]

bot_db_program = [(1, 'Вступительные мероприятия', '09:00 Регистрация', '09:00-10:00 Регистрация'), 
                  (2, 'Вступительные мероприятия', '10:00 Дискуссия - Пути развития рынка разработки', 
                  '''10:00 – 11:30 Планерная дискуссия – пути развития рынка разработки.    
                  Модератор: Иванов Иван независимый эксперт    Рынок интерактивной рекламы в России.  
                  Фёдор Федоров, партнер, Data Insight, Вице-президент IBF    
                  От телефона к автоматизации всей коммуникации.  
                  Денис Денисов, заместитель генерального директора, 
                  FMNT    Трансформация и автоматизация IT  Борис Борисов, 
                  Главный консультант, Россия Вперед    
                  ЭКСПЕРТЫ СЕССИИ:  Виталий Витальев, независимый эксперт  
                  Сергей Сергеев, заместитель генерального директора, 2F  Константин Константинов, евангелист, Birma'''), 
                  (3, 'Вступительные мероприятия', '11:30 Нетворкинг', 
                  '11:30 – 12:00 Перерыв, Нетворкинг, участие в зоне эксмпо')]                   

load_dotenv()
TG_TOKEN = os.environ.get("TG_TOKEN")

# Keyboards_functions #
def start(update, context):
    update.message.reply_text(
        main_menu_message(),
        reply_markup=main_menu_keyboard()
    )


def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=main_menu_message(),
        reply_markup=main_menu_keyboard()
    )


def programm_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=program_message(),
        reply_markup=programm_keyboard()
    )


def ask_menu(update,context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
                          reply_markup=ask_keyboard())


def sub_programm_menu(bot, update):
    query = bot.callback_query
    query.answer()
    query.edit_message_text(
        text=sub_program_message(),
        reply_markup=sub_programm_keyboard()
    )


def sub_ask_menu(bot, update):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
                          reply_markup=sub_ask_keyboard())


############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [
            [
                InlineKeyboardButton("Программа", callback_data="prog_1"),
                InlineKeyboardButton('Задать вопрос', callback_data="ask_1"),
            ]
        ]
    return InlineKeyboardMarkup(keyboard)


def programm_keyboard():
    db_answer = db_to_json("SELECT DISTINCT top_block FROM bot_db_program")
    keyboard = [[InlineKeyboardButton(block, callback_data=f'prog_2_{num}') for num, block in enumerate(db_answer)]]
    return InlineKeyboardMarkup(keyboard)


def ask_keyboard():
    themes = []
    for program in bot_db_program:
        if program[1] not in themes:
            themes.append(program[1])
    keyboard = [[InlineKeyboardButton(theme, callback_data=f'ask_2_{num}') for num,theme in enumerate(themes)]]
    return InlineKeyboardMarkup(keyboard)


def sub_programm_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='prog_3_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='prog_3_2')],
                [InlineKeyboardButton('Главное меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def sub_ask_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='ask_3_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='ask_3_2')],
                [InlineKeyboardButton('Главное меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

# Messages #


def main_menu_message():
    return 'Здравствуйте. Это официальный бот по поддержке участников 🤖.'


def program_message():
    return "Выберите блок программы:"


def sub_program_message():
    return "Выберите время:"


def main():
    updater = Updater(TG_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(programm_menu, pattern='prog_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(ask_menu, pattern='ask_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(sub_programm_menu,
                                                        pattern='prog_2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(sub_ask_menu,
                                                        pattern='ask_2'))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
