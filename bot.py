import demoji

import config
import telebot
from telebot import types

import random

bot = telebot.TeleBot(config.token)

beer_dict = {}

class Beer:
    def __init__(self, name):
        self.name = name
        self.volume = None


# Обработка команды для старта
@bot.message_handler(commands=['go', 'start', 'help'])
def welcome(message):

    item1 = types.KeyboardButton('Выбрать пиво \U0001F37A')

    markup = types.ReplyKeyboardMarkup()
    markup.add(item1)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\n\nЯ - бот <b>{1.first_name}</b>. \n"
                     "Cоздан для того, "
                     "чтобы помочь тебе выбрать сорт и объем "
                     "любимого пивка! \U0001F37A".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def go_send_messages(message):
    if message.chat.type == 'private':
        if message.text == 'Выбрать пиво \U0001F37A':

            choose_a_name(message)


def choose_a_name(message):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        itemboo0 = types.InlineKeyboardButton("Золотистое (фильтрованное)", callback_data='golden')
        itemboo1 = types.InlineKeyboardButton("Янтарное (фильтрованное)", callback_data='amber_f')
        itemboo2 = types.InlineKeyboardButton("Янтарное (нефильтрованное)", callback_data='amber_nf')
        itemboo3 = types.InlineKeyboardButton("Темное", callback_data='dark')

        keyboard.add(itemboo0, itemboo1, itemboo2, itemboo3)

        bot.send_message(message.chat.id,
                         "{0.first_name}, смотри, что у нас есть тут:\n".format(message.from_user),
                         # "Смотри, что у нас есть тут:\n".format(message.from_user),
                         reply_markup=keyboard)

    except Exception as error:
        bot.reply_to(message, repr(error))

@bot.callback_query_handler(func=lambda call: call.data in ['golden', 'amber_f', 'amber_nf', 'dark'])
def callback_inline_three(call):
    try:
        if call.message:
            chat_id = call.message.chat.id
            if call.data == 'golden':
                name = 'Золотистое (фильтрованное)'

            elif call.data == 'amber_f':
                name = 'Янтарное (фильтрованное)'

            elif call.data == 'amber_nf':
                name = 'Янтарное (нефильтрованное)'

            elif call.data == 'dark':
                name = 'Темное'

            beer = Beer(name)
            beer_dict[chat_id] = beer

            bot.send_message(call.message.chat.id, name)
            bot.send_message(call.message.chat.id, "Какой объем?", reply_markup=None)
            bot.register_next_step_handler(call.message, get_volume)

    except Exception as error:
        bot.reply_to(call.message, repr(error))


def get_volume(message):
    try:
        chat_id = message.chat.id
        volume = message.text
        if not volume.isdigit():
            msg = bot.reply_to(message, 'Цифрами, пожалуйста. Какой объем?')
            bot.register_next_step_handler(msg, get_volume)
            return
        beer = beer_dict[chat_id]
        beer.volume = volume
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_yes, key_no)
        question = 'Твой заказ: ' + str(beer.volume) + ' л. пива ' + beer.name + '. Подтверждаешь?'
        bot.send_message(message.chat.id, question, reply_markup=keyboard)
    except Exception as error:
        bot.reply_to(message, repr(error))


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def callback_inline_three(call):
    try:
        if call.message:
            if call.data == 'yes':
                bot.send_message(call.message.chat.id, 'Заказ принят!')

            elif call.data == 'no':
                bot.send_message(call.message.chat.id, 'Заказ не принят!')

    except Exception as error:
        bot.reply_to(call.message, repr(error))


# Обработка команды для выхода
@bot.message_handler(commands=['stop'])
def bye(message):

    hideBoard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                     "До свидания, {0.first_name}! \U0001F37B".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=hideBoard)
    exit()


# RUN
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
    except Exception as r:
        print("Непридвиденная ошибка: ", r)
    finally:
        print("Здесь всё закончилось")
