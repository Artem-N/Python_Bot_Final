import json
import requests
import wikipedia.exceptions
from flask import request
from bs4 import BeautifulSoup
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, \
    ConversationHandler, Filters
from wikipedia.exceptions import PageError, DisambiguationError

from app.all_massage_handler import get_image_url
from app.news_parsers import parse_politics, parse_avto, parse_sience, parse_sports, parse_technology, parse_economics
from app.pinterest_parser import parse_pinterest_cats, parse_pinterest_dogs, parse_pinterest_mems
from app.reddit_parser import parse_reddit_new, parse_reddit_hot, parse_reddit_top
from app.wiki_parser import search_wiki
from app import flask_app, Config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

WIKI = 1


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привіт {update.effective_user.username}'
                                                                    f', проходьте, почувайте себе як вдома!'
                                                                    f' Оберіть чим хочете поцікавитись наразі.')
    update.message.reply_text(text='Оберіть один із варіантів: ', reply_markup=main_menu_keyboard())


def menu_command(update: Update, context: CallbackContext):
    update.message.reply_text(text='Оберіть один із варіантів: ', reply_markup=main_menu_keyboard())


def help_(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Цей бот створено в навчальних цілях, завдяки ньому ви можете дізнатись інформацію '
                                  'з його розділів. Для отримання інформації натисніть кнопку: /menu. '
                                  'Щоб розпочати все заново натисніть кнопку: /start. В розділі "Wikipedia" ви можете запитати мене все що вас цікавить.')


def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Оберіть один із варіантів: ',
                             reply_markup=main_menu_keyboard())


def news_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=query.message.chat_id,
                             text='Оберіть що цікавить з новин: ',
                             reply_markup=news_menu_keyboard())


def snetwork_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=query.message.chat_id,
                             text='В якій соціальній мережі хочеш поритись?: ',
                             reply_markup=snetwork_menu_keyboard())


def fun_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=query.message.chat_id,
                             text='Що вам може підняти настрій?: ',
                             reply_markup=fun_menu_keyboard())


def wiki_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=query.message.chat_id,
                             text='Щоб покинути діалог натисни внизу',
                             reply_markup=wiki_menu_keyboard())


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Свіжі новини ⏰📰', callback_data='News')],
                [InlineKeyboardButton('Соціальні мережі 📱', callback_data='Social Network')],
                [InlineKeyboardButton('Розваги 🗿', callback_data='Fun')],
                [InlineKeyboardButton('Wikipedia 🧠', callback_data='Wiki')]]
    return InlineKeyboardMarkup(keyboard)


def news_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Політика 👨‍💼', callback_data='Politic')],
                [InlineKeyboardButton('Економіка 💸', callback_data='Economy')],
                [InlineKeyboardButton('Спорт 🏋️', callback_data='Sport')],
                [InlineKeyboardButton('Наука 🔭 ', callback_data='Sience')],
                [InlineKeyboardButton('Технології 🚀', callback_data='Technology')],
                [InlineKeyboardButton('Авто 🏎', callback_data='Auto')],
                [InlineKeyboardButton('Головне меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def snetwork_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Reddit Hot Posts 🔥 ', callback_data='Reddit Hot')],
                [InlineKeyboardButton('Reddit New Posts 🆕', callback_data='New Reddit')],
                [InlineKeyboardButton('Reddit Top Posts 🔝', callback_data='Top Reddit')],
                [InlineKeyboardButton('Головне меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def fun_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Котики 🐈', callback_data='Cats')],
        [InlineKeyboardButton('Собачки 🐕', callback_data='Dogs')],
        [InlineKeyboardButton('Посміятись би 🌝 ...', callback_data='Mems')],
        [InlineKeyboardButton('Головне меню', callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)


def wiki_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Головне меню', callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)


def handler_news_politic(update: Update, context: CallbackContext):
    news = parse_politics()
    if news:
        for pol in news:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{pol['time']}: {pol['title']}!\nМедіа: {pol['publishing']}\nLink: {pol['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=news_menu_keyboard())


def handler_news_economy(update: Update, context: CallbackContext):
    news = parse_economics()
    if news:
        for eco in news:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{eco['time']}: {eco['title']}!\nМедіа: {eco['publishing']}\nLink: {eco['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=news_menu_keyboard())


def handler_news_sport(update: Update, context: CallbackContext):
    news = parse_sports()
    if news:
        for spo in news:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{spo['time']}: {spo['title']}!\nМедіа: {spo['publishing']}\nLink: {spo['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=news_menu_keyboard())


def handler_news_sience(update: Update, context: CallbackContext):
    news = parse_sience()
    if news:
        for sie in news:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{sie['time']}: {sie['title']}!\nМедіа: {sie['publishing']}\nLink: {sie['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=news_menu_keyboard())


def handler_news_technology(update: Update, context: CallbackContext):
    news = parse_technology()
    if news:
        for tch in news:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{tch['time']}: {tch['title']}!\nМедіа: {tch['publishing']}\nLink: {tch['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=news_menu_keyboard())


def handler_news_avto(update: Update, context: CallbackContext):
    news = parse_avto()
    if news:
        for avt in news:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{avt['time']}: {avt['title']}!\nМедіа: {avt['publishing']}\nLink: {avt['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=news_menu_keyboard())


def handler_cats(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Починаю шукати котиків (◕‿◕)')
    cats = parse_pinterest_cats()
    if cats:
        for pin in cats:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Тут можна зберегти картинку -> {pin}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Якщо хочеться ще веселощів - вам сюди ↓ ',
                             reply_markup=fun_menu_keyboard())


def handler_dogs(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Починаю шукати собачок (^人^)')
    dogs = parse_pinterest_dogs()
    if dogs:
        for pin in dogs:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Тут можна зберегти картинку -> {pin}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Якщо хочеться ще веселощів - вам сюди ↓ ',
                             reply_markup=fun_menu_keyboard())


def handler_mems(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Починаю шукати меми (´｡• ᵕ •｡)')
    mems = parse_pinterest_mems()
    if mems:
        for pin in mems:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Тут можна зберегти картинку -> {pin}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Якщо хочеться ще веселощів - вам сюди ↓ ',
                             reply_markup=fun_menu_keyboard())


def handler_reddit_hot(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Заходжу на reddit ... ')
    red_hot = parse_reddit_hot()
    if red_hot:
        for data in red_hot:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Час публікації: {data['time']}\nЗаголовок -> {data['title']}.\nКількість коментарів: {data['comment']}\nLink: {data['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=snetwork_menu_keyboard())


def handler_reddit_new(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Заходжу на reddit ... ')
    red_new = parse_reddit_new()
    if red_new:
        for data in red_new:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Час публікації: {data['time']}\nЗаголовок -> {data['title']}.\nКількість коментарів: {data['comment']}\nLink: {data['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=snetwork_menu_keyboard())


def handler_reddit_top(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Заходжу на reddit ... ')
    red_top = parse_reddit_top()
    if red_top:
        for data in red_top:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Час публікації: {data['time']}\nЗаголовок -> {data['title']}.\nКількість голосів: {data['number_vote']}.\nКількість коментарів: {data['comment']}\nLink: {data['link']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Виникла проблема із сервером, спробуйте обрати ще раз!')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оберіть чим би ще поцікавитись 🧐: ',
                             reply_markup=snetwork_menu_keyboard())


def handler_wikipedia_start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='↓ Введіть необхідну для пошуку інформацію нижче, краще розумію російську мову(￢_￢) ↓',
                             reply_markup=wiki_menu_keyboard())
    return WIKI


def handl_message_wiki(update: Update, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Починаю пошук на wikipedia ... ')
        wiki = search_wiki(update.effective_message.text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=wiki, reply_markup=wiki_menu_keyboard())
    except (PageError, DisambiguationError):
        return context.bot.send_message(chat_id=update.effective_chat.id,
                                        text="Вибачте, трапилась халепка, спробуйте зайти ще раз в цей розділ і зробити конкретніший запит (⌒‿⌒)",
                                        reply_markup=wiki_menu_keyboard())


def massege_handler(update: Update, context: CallbackContext):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Вибачте(o˘◡˘o),але я не вмію тут спілкуватись, оберіть щось із /menu, або отримайте допомогу /help')


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text('Да прибуде з тобою сила знань ( ° ∀ ° )ﾉﾞ!', reply_markup=main_menu_keyboard())
    return ConversationHandler.END


@flask_app.route('/', methods=['GET', 'POST'])
def init_bot():
    updater = Updater(token=Config.TOKEN_BOT, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(handler_wikipedia_start, pattern='Wiki')
        ],
        states={
            WIKI: [
                MessageHandler(Filters.text & (~Filters.command), handl_message_wiki)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(cancel, pattern='main')
        ]
    )
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, massege_handler))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_))
    dispatcher.add_handler(CommandHandler('menu', menu_command))
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dispatcher.add_handler(CallbackQueryHandler(news_menu, pattern='News'))
    dispatcher.add_handler(CallbackQueryHandler(snetwork_menu, pattern='Social Network'))
    dispatcher.add_handler(CallbackQueryHandler(fun_menu, pattern='Fun'))
    dispatcher.add_handler(CallbackQueryHandler(handler_news_politic, pattern='Politic'))
    dispatcher.add_handler(CallbackQueryHandler(handler_news_economy, pattern='Economy'))
    dispatcher.add_handler(CallbackQueryHandler(handler_news_sport, pattern='Sport'))
    dispatcher.add_handler(CallbackQueryHandler(handler_news_sience, pattern='Sience'))
    dispatcher.add_handler(CallbackQueryHandler(handler_news_technology, pattern='Technology'))
    dispatcher.add_handler(CallbackQueryHandler(handler_news_avto, pattern='Auto'))
    dispatcher.add_handler(CallbackQueryHandler(handler_reddit_hot, pattern='Reddit Hot'))
    dispatcher.add_handler(CallbackQueryHandler(handler_reddit_new, pattern='New Reddit'))
    dispatcher.add_handler(CallbackQueryHandler(handler_reddit_top, pattern='Top Reddit'))
    dispatcher.add_handler(CallbackQueryHandler(handler_cats, pattern='Cats'))
    dispatcher.add_handler(CallbackQueryHandler(handler_dogs, pattern='Dogs'))
    dispatcher.add_handler(CallbackQueryHandler(handler_mems, pattern='Mems'))

    updater.start_polling()
    return 'Bot ready to work'
