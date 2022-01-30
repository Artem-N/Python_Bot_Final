from flask import request

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler

from app import flask_app, Config


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привіт {update.effective_user.username}'
                                                                    f', проходь, розувайся, почувай себе як вдома!')


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Цей бот створено для отримання інформації'
                                                                    ' яку він може надати шляхом натискання'
                                                                    ' відповідних кнопок з чату.')


def choose_button(update: Update):
    keyboard = [
        [InlineKeyboardButton('Глянути що у світі відбувається!', callback_data='1')],
        [InlineKeyboardButton('Про що гудуть соціальні мережі!', callback_data='2')],
        [InlineKeyboardButton('По всякі прикольчики', callback_data='3')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Отже, по що ти до мене прийшов? ', reply_markup=reply_markup)


def button(update: Update):
    query = update.callback_query
    variant = query.data
    query.answer()
    query.edit_message_text(text=f'Ти обрав: {variant}')


@flask_app.route('/init-bot', methods=['GET', 'POST'])
def init_bot():
    updater = Updater(token=Config.TOKEN_BOT, use_context=True)
    dispatcher = updater.dispatcher

    start_cmd = CommandHandler('start', start)
    help_cmd = CommandHandler('help', help)

    dispatcher.add_handler(start_cmd)
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(help_cmd)

    updater.start_polling()
    updater.idle()
    return 'Bot started'
