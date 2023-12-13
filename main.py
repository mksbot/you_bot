# -*- coding: utf-8 -*-
"""
This Example will show you an advanced usage of CallbackData.
In this example calendar was implemented
"""
import asyncio
import os
import sys
import time
from datetime import date
from pprint import pprint

from pytube import Search, YouTube
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackDataFilter

from filters import calendar_factory, calendar_zoom, bind_filters
from fun.arquivos_texto import abrir_reg
from fun.solicitaçoes import baixarmp3
from keyboards import EMTPY_FIELD, botao, pesquisas, products_keyboard, products_factory, \
    back_keyboard
from telebot import types
from telebot.async_telebot import AsyncTeleBot

API_TOKEN = '6159093978:AAEyVQZYRBA2YYkX6GNwl9ypGBWHYGUwNz4'
bot = AsyncTeleBot(API_TOKEN)

print('ESPERANDO..')
@bot.message_handler(commands='start')
async def start_command_handler(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Hello {message.from_user.first_name}. This bot is an example of calendar keyboard."
                           "\nPress /calendar to see it.")


@bot.callback_query_handler(func=lambda call: call.data == EMTPY_FIELD)
async def botaos(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                        reply_markup=botao())


@bot.message_handler(func=lambda message: True)
async def products_command_handler(message: types.Message):
    texto = message.text
    if 'https' in texto:
        await bot.send_message(message.chat.id, '🧿 Escolha Um Formato! 👇', reply_markup=products_keyboard(texto))


@bot.inline_handler(lambda query: query.query)
async def query_text(inline_query):
    try:

        await bot.answer_inline_query(inline_query.id, pesquisas(inline_query.query))
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: len(query.query) is 0)
async def default_query(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'digite sua pesquisa',
                                           types.InputTextMessageContent('Sigite sua busca'))
        await bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=None, config=products_factory.filter())
async def products_callback(call: types.CallbackQuery):
    callback_data: dict = products_factory.parse(callback_data=call.data)
    product_id = int(callback_data['product_id'])
    lk = abrir_reg('info')
    product = lk[product_id]
    print(call.message.text)
    text = f"{product['nome']}"
    itag = product['itag']
    ms = call.message.id
    link = product['link']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text, reply_markup=back_keyboard())
    markup = await bot.reply_to(call.message, '💾  Baixando.... ⏳'.upper())
    nome = baixarmp3(link, itag)
    await bot.edit_message_text('🌐 Enviando.... ♻️'.upper(), markup.chat.id, markup.message_id)

    musica = open(nome, 'rb')
    await bot.send_audio(call.message.chat.id, musica), bot.edit_message_text('🌐 Enviando....'.upper(), markup.chat.id, markup.message_id)
    await bot.edit_message_text(' ✅'.upper(), markup.chat.id, markup.message_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🧿 Enviado '
                                                                                                       'com Sucesso ✔️',
                                reply_markup=products_keyboard())
    # os.remove('info.json')
    musica.close()
    os.remove(nome)


@bot.callback_query_handler(func=lambda c: c.data == 'back')
async def back_callback(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🧿 Escolha Um '
                                                                                                       'Formato 👇',
                                reply_markup=products_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == EMTPY_FIELD)
async def callback_empty_field_handler(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)


class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    async def check(self, message: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=message)
bot.add_custom_filter(ProductsCallbackFilter())
if __name__ == '__main__':
    bind_filters(bot)
    asyncio.run(bot.infinity_polling())
