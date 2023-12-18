# -*- coding: utf-8 -*-
"""
This Example will show you an advanced usage of CallbackData.
In this example calendar was implemented
"""
import asyncio
import os
import random
import time
from pprint import pprint
from filters import bind_filters
from fun.arquivos_texto import abrir_reg, registro
from keyboards import EMTPY_FIELD, botao, pesquisas, enviar
from telebot import types
from telebot.async_telebot import AsyncTeleBot

API_TOKEN2 = '6799405184:AAG3tWe_OApTS_TzC2-7GZu53_sc36d8pFc'
bot = AsyncTeleBot(API_TOKEN2)

print('ESPERANDO..')


@bot.inline_handler(lambda query: query.query)
async def query_text(inline_query):
    try:

        await bot.answer_inline_query(inline_query.id, pesquisas(inline_query.query))
    except Exception as e:
        print(e)


# @bot.callback_query_handler(func=lambda call: call.data == EMTPY_FIELD)
# async def products_callback(call: types.CallbackQuery):
#     id_arq = (int(call.message.id) - 2)
#     markup = await bot.reply_to(call.message, '💾  Baixando.... ⏳'.upper())
#     c = 0
#
#     async def enviar(c):
#         try:
#             nome = abrir_reg(f'{id_arq}')
#             musica = open(nome, 'rb')
#         except:
#             time.sleep(1)
#             await bot.edit_message_text(f'🌐 Enviando....{"." * c}♻️'.upper(), markup.chat.id,
#                                         markup.message_id)
#             print('tentando')
#             c += 1
#             await enviar(c)
#         else:
#             await bot.edit_message_text('🌐 Enviando....♻️'.upper(), markup.chat.id,
#                                         markup.message_id)
#
#             await bot.send_audio(call.message.chat.id, musica)
#             await bot.edit_message_text(' ✅'.upper(), markup.chat.id, markup.message_id)
#             await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                         text='🧿 Enviado '
#                                              'com Sucesso ✔️',
#                                         reply_markup=botao())
#             # os.remove('info.json')
#             musica.close()
#             os.remove(nome)
#
#     await enviar(c)
#
#
@bot.message_handler(func=lambda message: True)
async def products_command_handler(message: types.Message):
    id_arq = f'{message.id}'
    texto = message.text
    if 'https' in texto:
        markup = await bot.reply_to(message, 'Analizando o link.... ⏳'.upper())
        await bot.delete_message(message.chat.id, message.id)
        lista2 = enviar(texto)
        if f'{len(lista2)}' not in '0':
            await bot.edit_message_text('🌐 Enviando....♻️'.upper(), markup.chat.id,
                                                    markup.message_id)
            for num, it in enumerate(lista2):
                descriçao, botao2, imagem = lista2[num]
                print('>> ENVIANDO !!')
                time.sleep(random.randint(0, 2))

                await bot.send_photo(message.chat.id, f'{imagem}', caption=f'{descriçao}', reply_markup=botao2)
            await bot.edit_message_text('🧿 Enviado com Sucesso ✔️', markup.chat.id, markup.message_id)
            await bot.reply_to(markup, ' ✅'.upper())





@bot.inline_handler(lambda query: len(query.query) is 0)
async def default_query(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Pesquise seu anime favorito:\n'
                                                'Exemplo de Uso:👇\n\n'
                                                '🔎 digite: @Ani_pesgbot naruto\n\n'
                                                '❗️Não envie a msg)❗️\n\n'
                                           ,
                                           types.InputTextMessageContent('🔎 Pesquise seu anime favorito que enviarei para você! 🌐\n\n'
                                                                         'Exemplo de Uso:👇\n\n'
                                                                         '🔎 digite: @Ani_pesgbot naruto\n\n'
                                                                         '❗️Não envie a msg)❗️\n\n'
                                                                         '👉Vai aparecer uma lista com os animes na tela: clique no anime e pronto!'),thumbnail_url='https://99designs-blog.imgix.net/blog/wp-content/uploads/2019/10/c1c70663-e19b-4db4-b9e4-caf805d16112-e1571876620702.jpg?auto=format&q=60&fit=max&w=930')
        await bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


# @bot.message_handler(commands='start')
# async def start_command_handler(message: types.Message):
#     await bot.send_message(message.chat.id,
#                            f"Hello {message.from_user.first_name}. This bot is an example of calendar keyboard."
#                            "\nPress /calendar to see it.")
#
#
@bot.message_handler(commands='QUITT')
async def start_command_handler(message: types.Message):
    quit()


# # @bot.callback_query_handler(func=lambda call: call.data == EMTPY_FIELD)
# # async def botaos(call: types.CallbackQuery):
# #     await bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
# #                                         reply_markup=botao())
#
#
# # @bot.callback_query_handler(func=lambda c: c.data == 'back')
# # async def back_callback(call: types.CallbackQuery):
# #     await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🧿 Escolha Um '
# #                                                                                                        'Formato 👇',
# #                                 reply_markup=products_keyboard())
#
#
if __name__ == '__main__':
    bind_filters(bot)
    asyncio.run(bot.infinity_polling())
