import os
import telegram
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

speakers = [
    [3, "1070225969", "Riches Starkoni", "50 shades of API in Python", "2022-07-28 20:20:00", "2022-07-28 20:25:00"],
    [4, "171951902", "MrSabin", "Zen of Django ORM", "2022-07-28 20:25:00", "2022-07-28 20:30:00"]]
# Этапы/состояния разговора
FIRST, SECOND = range(2)
# Данные обратного вызова
ONE, TWO, THREE, FOUR = range(4)


def add_text_speaker():
    text = f'С докладом сегодня выступает:\n'
    for i in speakers:
        text2 =f'Спикер {i[2]}, на тему "{i[3]}", начало {i[4]}, конец {i[5]}\n'
        text = text + text2
    return text


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
    keyboard = [[InlineKeyboardButton(name[2], callback_data=name[1]) for name in speakers],
        [
            InlineKeyboardButton("Описание программы", callback_data=str(ONE)),
            InlineKeyboardButton("F.A.Q", callback_data=str(THREE)),
            InlineKeyboardButton("Покинуть", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
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
    load_dotenv()
    chat_id = os.environ.get('CHAT_ID')
    tg_token = os.environ.get("TG_TOKEN")
    bot = telegram.Bot(token=tg_token)
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    # Настройка обработчика разговоров с состояниями `FIRST` и `SECOND`
    # Используем параметр `pattern` для передачи `CallbackQueries` с
    # определенным шаблоном данных соответствующим обработчикам
    # ^ - означает "начало строки"
    # $ - означает "конец строки"
    # Таким образом, паттерн `^ABC$` будет ловить только 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={  # словарь состояний разговора, возвращаемых callback функциями
            FIRST: [
                CallbackQueryHandler(open_menu, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(open_speakers, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(open_faq, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(FOUR) + '$'),
            ],
            SECOND: [

            ],
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
