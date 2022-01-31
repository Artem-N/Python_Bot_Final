from flask import request

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler

from app import flask_app, Config


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привіт {update.effective_user.username}'
                                                                    f', проходь, розувайся, почувай себе як вдома!'
                                                                    f' Обери чим хочеш поцікавитись сьогодні.')
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def menu_command(update: Update, context: CallbackContext):
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=main_menu_message(),
                                  reply_markup=main_menu_keyboard())


def first_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=first_menu_message(),
                                  reply_markup=first_menu_keyboard())


def second_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
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
    context.bot.send_message(chat_id=update.effective_chat.id, text='Цей бот створено для отримання інформації')


@flask_app.route('/init-bot', methods=['GET', 'POST'])
def init_bot():
    updater = Updater(token=Config.TOKEN_BOT, use_context=True)
    dispatcher = updater.dispatcher

    start_cmd = CommandHandler('start', start)
    help_cmd = CommandHandler('help', help_)
    menu_cmd = CommandHandler('menu', menu_command)

    dispatcher.add_handler(start_cmd)
    dispatcher.add_handler(help_cmd)
    dispatcher.add_handler(menu_cmd)
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))

    updater.start_polling()
    return 'Bot started'
