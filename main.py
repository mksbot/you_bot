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
from fun.arquivos_texto import abrir_reg, registro
from keyboards import EMTPY_FIELD, botao, pesquisas
from telebot import types
from telebot.async_telebot import AsyncTeleBot

API_TOKEN = '6159093978:AAEyVQZYRBA2YYkX6GNwl9ypGBWHYGUwNz4'
bot = AsyncTeleBot(API_TOKEN)

print('ESPERANDO..')


@bot.inline_handler(lambda query: query.query)
async def query_text(inline_query):
    try:

        await bot.answer_inline_query(inline_query.id, pesquisas(inline_query.query))
    except Exception as e:
        print(e)


class Baixar:
    def status(self):
        print(self.yt.title + " Baixado com sucesso")

    def info(self):
        return self.yt.title, self.yt.thumbnail_url

    def baixa(self):
        yt = self.yt.streams.filter(only_audio=True, abr='128kbps').first()
        pprint(yt.itag)

        out_file = yt.download()
        return out_file

    def __init__(self, link):
        self.yt = YouTube(link)


@bot.callback_query_handler(func=lambda call: call.data == EMTPY_FIELD)
async def products_callback(call: types.CallbackQuery):
    id_arq = (int(call.message.id) - 2)
    markup = await bot.reply_to(call.message, '💾  Baixando.... ⏳'.upper())
    c = 0

    async def enviar(c):
        try:
            nome = abrir_reg(f'{id_arq}')
            musica = open(nome, 'rb')
        except:
            time.sleep(1)
            await bot.edit_message_text(f'🌐 Enviando....{"." * c}♻️'.upper(), markup.chat.id,
                                        markup.message_id)
            print('tentando')
            c += 1
            await enviar(c)
        else:
            await bot.edit_message_text('🌐 Enviando....♻️'.upper(), markup.chat.id,
                                        markup.message_id)

            await bot.send_audio(call.message.chat.id, musica)
            await bot.edit_message_text(' ✅'.upper(), markup.chat.id, markup.message_id)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='🧿 Enviado '
                                             'com Sucesso ✔️',
                                        reply_markup=botao())
            # os.remove('info.json')
            musica.close()
            os.remove(nome)

    await enviar(c)


@bot.message_handler(func=lambda message: True)
async def products_command_handler(message: types.Message):
    id_arq = f'{message.id}'
    texto = message.text
    if 'https' in texto:
        nome, imagem = Baixar(texto).info()
        print(imagem)
        await bot.send_photo(message.chat.id, f'{imagem}', f'{nome}')
        await bot.send_message(message.chat.id, '🧿 Escolha Um Formato! 👇',
                               reply_markup=botao())
        nome = Baixar(texto).baixa()
        registro(nome, id_arq)


@bot.inline_handler(lambda query: len(query.query) is 0)
async def default_query(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'digite sua pesquisa',
                                           types.InputTextMessageContent('Sigite sua busca'))
        await bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


@bot.message_handler(commands='start')
async def start_command_handler(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Hello {message.from_user.first_name}. This bot is an example of calendar keyboard."
                           "\nPress /calendar to see it.")


@bot.message_handler(commands='QUITT')
async def start_command_handler(message: types.Message):
    quit()


# @bot.callback_query_handler(func=lambda call: call.data == EMTPY_FIELD)
# async def botaos(call: types.CallbackQuery):
#     await bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
#                                         reply_markup=botao())


# @bot.callback_query_handler(func=lambda c: c.data == 'back')
# async def back_callback(call: types.CallbackQuery):
#     await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🧿 Escolha Um '
#                                                                                                        'Formato 👇',
#                                 reply_markup=products_keyboard())


if __name__ == '__main__':
    bind_filters(bot)
    asyncio.run(bot.infinity_polling())
