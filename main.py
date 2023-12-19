import asyncio
import random
import telebot
import time

from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot.util import quick_markup

from filters import bind_filters
from fun.arquivos_texto import registro, abrir_reg
import requests
from bs4 import BeautifulSoup

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


async def calendario_a():
    chat_testes = -1002073463326
    chat = -1002000136655
    # ANIMES LEGENDADOS
    page = f'https://animesonlinecc.to/episodio/page/0/'
    print(page)
    hesders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}

    site = requests.get(page, headers=hesders)
    soup = BeautifulSoup(site.content.decode('utf-8'), 'html.parser')
    magnet2 = soup.find_all('div', class_='animation-2 items')
    i = 1
    lista = []
    lista_dub = []

    for v in magnet2[0]:

        lista2 = []
        informaçoes = str(v.text).replace('do ', 'do >')
        num = informaçoes.find('>')
        nome = informaçoes[num + 1:]
        num = nome.find('Episodio')
        episodio = nome[num:]
        nome = nome[:num].upper()
        mau_elementos = (
            "a,b,c,ç,Ç,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,"
            "Y,Z,À,Á,Â,Ä,Å,Ã,Æ,Ç,É,È,Ê,Ë,Í,Ì,Î,Ï,Ñ,Ó,Ò,Ô,Ö,Ø,Õ,O,E,Ú,Ù,Û,Ü,Ý,Y à,á,â,ä,å,ã,æ,ç,é,è,ê,ë,í,ì,î,ï,ñ,ó,ò,"
            "ô,ö,ø,õ,o,e,ú,ù,û,ü,ý,y".replace(',', ' ').split())
        tag = ''
        for c in nome:
            if c not in mau_elementos:
                if tag == '':
                    tag = nome.replace(str(c), '_')
                else:
                    tag = tag.replace(str(c), '_')
        idioma = informaçoes[1:5].upper()
        descriçao = (f'> Fonte--1'
                     f'\n\n'
                     f'     ✅{nome}\n'
                     f'{"_" * (len(nome) + 10)}\n\n'
                     f'#{tag[:24].replace("__", "_")}..\n'
                     f'🎞{episodio}   |   '
                     f'🇧🇷{idioma}'
                     )
        # print(descriçao)
        try:
            reg = abrir_reg('animes')
        except:
            registro(f'{nome}{episodio}', 'animes', 'nao')
            reg = abrir_reg('animes')
        if str(nome + episodio) not in reg:
            lista2.append(descriçao)
            for c in v.div:

                try:
                    link = c['href']
                    site = requests.get(link, headers=hesders)
                    soup = BeautifulSoup(site.content.decode('utf-8'), 'html.parser')
                    magnet2 = soup.find_all('div', class_='play-box-iframe fixidtab')
                    link2 = magnet2[0].iframe['src']

                    imagem = c.img['src']
                    botao = quick_markup({

                        'ASSISTIR | BAIXAR': {'url': link2},

                    }, row_width=2)
                    lista2.append(botao)
                    lista2.append(imagem)
                    lista2.append(f'{nome + episodio}')
                    lista.append(lista2)



                except:
                    pass
        else:

            print('>> JA FOI ENVIADO !!')

    # # ANIMES DUBLADO
    # page = f'https://animefire.plus'
    # print(page)
    # hesders = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
    #                   'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}
    # site = requests.get(page, headers=hesders)
    # soup = BeautifulSoup(site.content, 'html.parser')
    # magnet2 = soup.find_all('div', class_='row ml-1 mr-1 mr-md-2')
    #
    # for v in magnet2[0]:
    #     lista2 = []
    #     informaçoes = str(v.text).replace('     ', '>')
    #     num = informaçoes.find('- E')
    #     episodio = informaçoes[num + 1:informaçoes.find('>', num)]
    #     nome = informaçoes[:num].replace(">", " ").upper()
    #
    #     mau_elementos = (
    #         "a,b,c,ç,Ç,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,"
    #         "Y,Z,À,Á,Â,Ä,Å,Ã,Æ,Ç,É,È,Ê,Ë,Í,Ì,Î,Ï,Ñ,Ó,Ò,Ô,Ö,Ø,Õ,O,E,Ú,Ù,Û,Ü,Ý,Y à,á,â,ä,å,ã,æ,ç,é,è,ê,ë,í,ì,î,ï,ñ,ó,ò,"
    #         "ô,ö,ø,õ,o,e,ú,ù,û,ü,ý,y".replace(',', ' ').split())
    #     tag = ''
    #     if 'Dub' in nome or 'DUB' in nome or 'dub' in nome:
    #         idioma = f'(DUB)'
    #     else:
    #         idioma = f'(LEG)'
    #     for c in nome:
    #         if c not in mau_elementos:
    #             if tag == '':
    #                 tag = nome.replace(str(c), '_')
    #             else:
    #                 tag = tag.replace(str(c), '_')
    #     descriçao = (f'> Fonte--2'
    #                  f'\n\n'
    #                  f'     ✅{nome}\n'
    #                  f'{"_" * (len(nome) + 10)}\n\n'
    #                  f'#{tag[:24].replace("__", "_")}..\n'
    #                  f'🎞{episodio}   |   '
    #                  f'🇧🇷{idioma}'
    #                  )
    #     # print(descriçao)
    #     try:
    #         reg = abrir_reg('animes')
    #     except:
    #         registro(f'{nome}{episodio}', 'animes', 'nao')
    #         reg = abrir_reg('animes')
    #
    #     if str(nome + episodio) not in reg:
    #         lista2.append(descriçao)
    #
    #         try:
    #             link = v.a['href']
    #             site = requests.get(link, headers=hesders)
    #             soup = BeautifulSoup(site.content, 'html.parser')
    #             magnet2 = soup.find_all('div', id='div_video', )
    #             for j in magnet2[0]:
    #                 try:
    #                     link2 = j.video['data-video-src']
    #                 except:
    #                     pass
    #
    #             tratar_link = requests.get(link2)
    #             links = str(tratar_link.text)
    #
    #             inicio = links.find('http', 150)
    #             if inicio <= -1:
    #                 if len(links) <= 160:
    #                     inicio = links.find('http')
    #                 else:
    #                     inicio = links.find('http', 30)
    #             fim = links.find('label', inicio)
    #             link3 = links[inicio:fim - 3].replace('\/', '/')
    #             imagem = v.img['data-src']
    #
    #             botao = quick_markup({
    #
    #                 'ASSISTIR | BAIXAR': {'url': link3},
    #
    #             }, row_width=2)
    #             lista2.append(botao)
    #             lista2.append(imagem)
    #             lista2.append(f'{nome + episodio}')
    #             lista.append(lista2)
    #
    #         except:
    #             pass
    #     else:
    #
    #         print('>> JA FOI ENVIADO !!')
    lista.reverse()
    if f'{len(lista)}' not in '0':
        for num, it in enumerate(lista):
            descriçao, botao, imagem, nomer = lista[num]
            print(nomer)
            print('>> ENVIANDO !!')
            await asyncio.sleep(random.randint(0, 1))
            if num % 2 == 0:
                bot2.send_photo(chat, f'{imagem}', caption=f'{descriçao}', reply_markup=botao)
            else:
                bot1.send_photo(chat, f'{imagem}', caption=f'{descriçao}', reply_markup=botao)
            registro(f'{nomer}', 'animes', 'nao')

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
