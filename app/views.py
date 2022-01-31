from flask import request

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler

from app import flask_app, Config


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привіт {update.effective_user.username}'
                                                                    f', проходь, розувайся, почувай себе як вдома!')
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=main_menu_message(),
                                  reply_markup=main_menu_keyboard())


def first_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=first_menu_message(),
                                  reply_markup=first_menu_keyboard())


def second_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=second_menu_message(),
                                  reply_markup=second_menu_keyboard())


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
                [InlineKeyboardButton('Option 2', callback_data='m2')],
                [InlineKeyboardButton('Option 3', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
                [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def main_menu_message():
    return 'Choose the option in main menu'


def first_menu_message():
    return 'Choose the submenu in first menu:'


def second_menu_message():
    return 'Choose the submenu in second menu:'


def help_(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Цей бот створено для отримання інформації'
                                                                    ' яку він може надати шляхом натискання'
                                                                    ' відповідних кнопок з чату.')


# def choose_button(update: Update):
#     keyboard = [
#         [InlineKeyboardButton('Глянути що у світі відбувається!', callback_data='1')],
#         [InlineKeyboardButton('Про що гудуть соціальні мережі!', callback_data='2')],
#         [InlineKeyboardButton('По всякі прикольчики', callback_data='3')],
#
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Отже, по що ти до мене прийшов? ', reply_markup=reply_markup)
#
#
# def button(update: Update):
#     query = update.callback_query
#     variant = query.data
#     query.answer()
#     query.edit_message_text(text=f'Ти обрав: {variant}')


@flask_app.route('/init-bot', methods=['GET', 'POST'])
def init_bot():
    updater = Updater(token=Config.TOKEN_BOT, use_context=True)
    dispatcher = updater.dispatcher

    start_cmd = CommandHandler('start', start)
    help_cmd = CommandHandler('help', help_)

    dispatcher.add_handler(start_cmd)
    dispatcher.add_handler(help_cmd)
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    # dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    return 'Bot started'
