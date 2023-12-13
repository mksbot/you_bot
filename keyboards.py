import calendar
from pprint import pprint

from youtubesearchpython import VideosSearch
from datetime import date, timedelta
from pytube import Search, YouTube

from telebot import types
from telebot.callback_data import CallbackData

from filters import calendar_factory, calendar_zoom
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from fun.arquivos_texto import registro, abrir_reg

EMTPY_FIELD = '1'
WEEK_DAYS = [calendar.day_abbr[i] for i in range(7)]
MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]
products_factory = CallbackData('product_id', prefix='products')


def pesquisas(texto):
    videosSearch = VideosSearch(texto, limit=40)
    pesquisar = dict(videosSearch.result())

    itens = []
    for n, v in enumerate(pesquisar['result']):
        thumbnail_url = v['thumbnails'][0]['url']
        titulo = v['title']
        url = v['link']
        # print(titulo, thumbnail_url)
        itens.append(types.InlineQueryResultArticle(f'{n}', f'{titulo}',
                                           types.InputTextMessageContent(url),
                                           thumbnail_url=f'{thumbnail_url}'))
    return itens


if __name__ == '__main__':
    print(pesquisas('funk'))


# def qualidade(link):
#     yt = YouTube(link)
#     dcn = lambda nm, el: {nm: el}
#     exten2 = []
#     try:
#         idd = int(abrir_reg('ids', True))
#     except:
#         idd = 0
#     for stream in yt.streams.filter(only_audio=True):
#         exten = {}
#         itag = stream.itag
#
#         # tip=f'{stream.mime_type}{str(stream)[str(stream).find("res=") + 4:(str(stream).find("res=") + 10)]}'.replace(
#         #         "\"", '|')
#
#         tip = f'🎙 MP3 | {stream.abr}'
#         exten.update(dcn('id', idd))
#         exten.update(dcn('nome', tip))
#         exten.update(dcn('itag', itag))
#         exten.update(dcn('link', link))
#         exten2.append(exten)
#         n = str(idd / 4)
#         print(idd)
#         if '75' in n:
#             print('>>', n)
#             idd += 1
#             break
#         else:
#             print('..')
#             idd += 1
#     registro(idd, 'ids', True)
#     registro(exten2, 'info')
#     item = abrir_reg('info')
#     marca = len(item)
#     cont = 0
#     itens = []
#     for it in item:
#         if cont > marca - 5:
#             itens.append(it)
#         cont += 1
#
#     return itens


def botao():
    botao2 = InlineKeyboardMarkup(row_width=7)
    from telebot.util import quick_markup

    botao2 = quick_markup({

        'Baixar MP3': {'callback_data': EMTPY_FIELD},

    }, row_width=2)
    # {
    #     'url': None,
    #     'callback_data': None,
    #     'switch_inline_query': None,
    #     'switch_inline_query_current_chat': None,
    #     'callback_game': None,
    #     'pay': None,
    #     'login_url': None,
    #     'web_app': None
    # }
    # botao2.add(
    #     InlineKeyboardButton(
    #         text='OLA EU ESTOU A TESTAR',
    #         callback_data=EMTPY_FIELD
    #     )
    # )
    return botao2


# def products_keyboard(link='', ids=0):
#     lk = qualidade(link)
#
#     return types.InlineKeyboardMarkup(
#         keyboard=[
#             [
#                 types.InlineKeyboardButton(
#                     text=product['nome'],
#                     callback_data=products_factory.new(product_id=product["id"])
#                 )
#             ]
#             for product in lk
#         ]
#     )
#

def back_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text='⬅',
                    callback_data='back'
                )
            ]
        ]
    )
