import asyncio
import random
import telebot
import time

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from fun.solicitacoes import restart, calendario_a, noticias
from filters import bind_filters


from keyboards import pesquisas, enviar

API_TOKEN = ['6812826133:AAHTh_ZzbOSXeKjAedxwpPKJMeuMt6AT-o8',
             '6859056897:AAFAhdg80DyiYjBX3lIKBzZ-xWaRqDDQGQ8']

API_TOKEN2 = '6799405184:AAG3tWe_OApTS_TzC2-7GZu53_sc36d8pFc'
bot = AsyncTeleBot(API_TOKEN2)
bot1 = telebot.TeleBot(API_TOKEN[0])
bot2 = telebot.TeleBot(API_TOKEN[1])


@bot.message_handler(commands='start')
async def start_command_handler(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Ola {message.from_user.first_name}. Para usat este bot entre no nosso grupo:\n https://t.me/+eGIsvENJighiNGNh ")


@bot.message_handler(commands='QUITT')
async def start_command_handler(message: types.Message):
    quit()


@bot.message_handler(commands='RR')
async def start_command_handler(message: types.Message):
    restart()



# -*- coding: utf-8 -*-
"""
This Example will show you an advanced usage of CallbackData.
In this example calendar was implemented
"""

print('ESPERANDO..')


@bot.inline_handler(lambda query: query.query)
async def query_text(inline_query):
    try:

        await bot.answer_inline_query(inline_query.id, pesquisas(inline_query.query))
    except Exception as e:
        print(e)



@bot.message_handler(func=lambda message: True)
async def products_command_handler(message: types.Message):
    print(message.chat.id)
    texto = message.text
    if 'animefire' in texto:
        markup = await bot.reply_to(message, 'Analizando o link.... ⏳'.upper())
        await bot.delete_message(message.chat.id, message.id)
        lista2 = enviar(texto)
        if f'{len(lista2)}' not in '0':
            await bot.edit_message_text('🌐 Enviando....♻️'.upper(), markup.chat.id,
                                        markup.message_id)

            botao2 = lista2[1]
            descriçao, imagem = lista2[0]
            print('>> ENVIANDO !!')
            time.sleep(random.randint(0, 2))
            await bot.send_photo(message.chat.id, f'{imagem}', caption=f'{descriçao}', reply_markup=botao2)
            await bot.edit_message_text('🧿 Enviado com Sucesso ✔️', markup.chat.id, markup.message_id)
            await bot.reply_to(markup, ' ✅'.upper())
    await calendario_a()
    await noticias()


@bot.inline_handler(lambda query: len(query.query) is 0)
async def default_query(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Pesquise seu anime favorito:\n'
                                                'Exemplo de Uso:👇\n\n'
                                                '🔎 digite: @Ani_pesgbot naruto\n\n'
                                                '❗️Não envie a msg)❗️\n\n'
                                           ,
                                           types.InputTextMessageContent(
                                               '🔎 Pesquise seu anime favorito que enviarei para você! 🌐\n\n'
                                               'Exemplo de Uso:👇\n\n'
                                               '🔎 digite: @Ani_pesgbot naruto\n\n'
                                               '❗️Não envie a msg)❗️\n\n'
                                               '👉Vai aparecer uma lista com os animes na tela: clique no anime e pronto!'),
                                           thumbnail_url='https://99designs-blog.imgix.net/blog/wp-content/uploads'
                                                         '/2019/10/c1c70663-e19b-4db4-b9e4-caf805d16112'
                                                         '-e1571876620702.jpg?auto=format&q=60&fit=max&w=930')
        await bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


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
