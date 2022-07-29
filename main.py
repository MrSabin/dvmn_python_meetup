import os
import datetime
import locale
import sqlite3
import telegram
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

locale.setlocale(locale.LC_ALL, "ru")
speakers = []

# Этапы/состояния разговора
FIRST, SECOND = range(2)
# Данные обратного вызова
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)


def process_the_message(update, context):
    text = 'Ваш вопрос отправлен'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)
    print(update)

def create_speakers_list(speakers):
    with sqlite3.connect('db.sqlite3') as db:
        cur = db.cursor()
    for i in cur.execute("SELECT * FROM bot_db_speaker;"):
        speakers.append(i)


def create_date(info):
    start_time = datetime.datetime.strptime(info[4], "%Y-%m-%d %H:%M:%S").strftime('%d %b %H:%M')
    finish_date = datetime.datetime.strptime(info[5], "%Y-%m-%d %H:%M:%S").strftime('%d %b %H:%M')
    return start_time, finish_date


def add_text_speaker():
    all_text = f'С докладом сегодня выступает:\n'
    n = 1
    for info in speakers:
        create_date(info)
        info_text =f'Спикер №{n} {info[2]}\n-Тема"{info[3]}"\n-Начало вещяния {create_date(info)[0]}\n' \
                   f'-Конец вещяния {create_date(info)[1]}\n'
        all_text = all_text + info_text
        n += 1
    return all_text


def send_message_for_speaker(update, _):
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("Докладчики", callback_data=str(TWO)),
            InlineKeyboardButton("Меню", callback_data=str(ONE))]
    ]

    theme_text = f"Напишите Ваш вопрос для докладчика"
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=theme_text, reply_markup=reply_markup
    )

    return FIRST

def theme_spiker(update, _):
    query = update.callback_query
    query.answer()
    for info in speakers:
        if info[1] == query.data:
            theme_text = f'Выбран {info[2]}\nТема доклада "{info[3]}"\n' \
                         f'Начало выступления {create_date(info)[0]}\n' \
                         f"Окончаниеи выступления {create_date(info)[1]}"
            keyboard = [
                    [InlineKeyboardButton("Задать вопрос", callback_data=str(FIVE))],
                    [InlineKeyboardButton("Докладчики", callback_data=str(TWO)),
                    InlineKeyboardButton("Меню", callback_data=str(ONE))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=theme_text, reply_markup=reply_markup
    )
    return FIRST


def start(update, _):
    """Вызывается по команде `/start`."""
    # Создаем `InlineKeyboard`, где каждая кнопка имеет
    # отображаемый текст и строку `callback_data`
    # Клавиатура - это список строк кнопок, где каждая строка,
    # в свою очередь, является списком `[[...]]`
    keyboard = [
        [
            InlineKeyboardButton("Докладчики", callback_data=str(TWO)),
            InlineKeyboardButton("F.A.Q", callback_data=str(THREE)),
            InlineKeyboardButton("Покинуть", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
    update.message.reply_text(
        text="Добро пожаловать на нашей встрече", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
    return FIRST


def open_menu(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Список докладчиков", callback_data=str(TWO)),
            InlineKeyboardButton("F.A.Q", callback_data=str(THREE)),
            InlineKeyboardButton("Покинуть", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    theme_text = "Тут из базы повестка нашей встречи"
    query.edit_message_text(
        text=theme_text, reply_markup=reply_markup
    )
    return FIRST


def open_speakers(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard_speaker = []
    for name in speakers:
        keyboard_speaker.append([InlineKeyboardButton(name[2], callback_data=str(name[1]))])
    keyboard_menu = [
            [InlineKeyboardButton("Описание программы", callback_data=str(ONE)),
            InlineKeyboardButton("F.A.Q", callback_data=str(THREE)),
            InlineKeyboardButton("Покинуть", callback_data=str(FOUR))],
        ]
    keyboard_total = keyboard_speaker + keyboard_menu
    reply_markup = InlineKeyboardMarkup(keyboard_total)
    query.edit_message_text(
        text=add_text_speaker(), reply_markup=reply_markup
    )
    return FIRST


def open_faq(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Описание программы", callback_data=str(ONE)),
            InlineKeyboardButton("Список докладчиков", callback_data=str(TWO)),
            InlineKeyboardButton("Покинуть", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Дополнительные материалы к встрече", reply_markup=reply_markup
    )
    return FIRST


def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    end_text = 'Спасибо, что слушаете нас'
    query.edit_message_text(text=end_text)
    return ConversationHandler.END


def main():
    add_text_speaker()
    load_dotenv()
    tg_token = os.environ.get("TG_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    create_speakers_list(speakers)
    first = [
                CallbackQueryHandler(open_menu, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(open_speakers, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(open_faq, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(FOUR) + '$'),
                CallbackQueryHandler(send_message_for_speaker, pattern='^' + str(FIVE) + '$'),
            ]
    for info_speaker in speakers:
        first.append(CallbackQueryHandler(theme_spiker, pattern='^' + str(info_speaker[1]) + '$'))


    # Настройка обработчика разговоров с состояниями `FIRST` и `SECOND`
    # Используем параметр `pattern` для передачи `CallbackQueries` с
    # определенным шаблоном данных соответствующим обработчикам
    # ^ - означает "начало строки"
    # $ - означает "конец строки"
    # Таким образом, паттерн `^ABC$` будет ловить только 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={  # словарь состояний разговора, возвращаемых callback функциями
            FIRST: first,
            SECOND: [
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )
    # Добавляем `ConversationHandler` в диспетчер, который
    # будет использоваться для обработки обновлений
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
