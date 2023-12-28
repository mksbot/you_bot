import random
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from telebot import types
from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telebot.util import quick_markup

from fun.arquivos_texto import registro, abrir_reg

EMTPY_FIELD = '1'

products_factory = CallbackData('product_id', prefix='products')
mau_elementos = (
                            "a,b,c,ç,Ç,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,"
                            "Y,Z,À,Á,Â,Ä,Å,Ã,Æ,Ç,É,È,Ê,Ë,Í,Ì,Î,Ï,Ñ,Ó,Ò,Ô,Ö,Ø,Õ,O,E,Ú,Ù,Û,Ü,Ý,Y à,á,â,ä,å,ã,æ,ç,é,è,ê,ë,í,ì,î,ï,ñ,ó,ò,"
                           "ô,ö,ø,õ,o,e,ú,ù,û,ü,ý,y".replace(',', ' ').split())

def pesquisas(texto):
    page = f'https://animefire.plus/pesquisar/{str(texto).replace(" ", "-")}'
    print(page)
    hesders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}

    site = requests.get(page, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='row ml-1 mr-1')
    lista_inline = []
    for v in magnet2[0]:
        try:
            nome = str(v['title']).replace('- Todos os Episódios', '')
        except:
            pass
        else:
            lista_inline2 = []
            link = v.a['href']
            imagem = v.a.img['data-src']

            lista_inline2.append(nome)
            lista_inline2.append(imagem)
            lista_inline2.append(link)
            lista_inline.append(lista_inline2)
    if len(magnet2[0])-3 >= 46:
        page = f'https://animefire.plus/pesquisar/{str(texto).replace(" ", "-")}/2'
        site = requests.get(page, headers=hesders)
        soup = BeautifulSoup(site.content, 'html.parser')
        magnet2 = soup.find_all('div', class_='row ml-1 mr-1')
        for v in magnet2[0]:
            try:
                nome = str(v['title']).replace('- Todos os Episódios', '')
            except:
                pass
            else:
                lista_inline2 = []
                link = v.a['href']
                imagem = v.a.img['data-src']

                lista_inline2.append(nome)
                lista_inline2.append(imagem)
                lista_inline2.append(link)
                lista_inline.append(lista_inline2)

    pesquisar = lista_inline
    itens = []
    for n, v in enumerate(pesquisar):
        titulo, thumbnail_url, url = pesquisar[n]
        if 'Dub' in titulo or 'DUB' in titulo or 'dub' in titulo:
            titulo = f'{titulo[:35]}(DUBLADO)'
        else:
            titulo = f'{titulo[:35]}(LEGENDADO)'
        print(titulo)
        itens.append(types.InlineQueryResultArticle(f'{n}', f'{titulo}',
                                                    types.InputTextMessageContent(url),
                                                    thumbnail_url=f'{thumbnail_url}'))
    return itens



def enviar(link):
    descriçao = ''
    tag = ''
    hesders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}
    site = requests.get(link, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='sub_animepage_img')
    lista2 = []
    for d in magnet2[0]:
        try:
            nome = d['alt']
            imagem = d['data-src']
            print(imagem, '\n',
                  nome)
        except:
            pass
    site = requests.get(link, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='div_video_list')
    cont = 0
    lista_botao = []
    lista = []

    if len(magnet2[0]) > 42:
        for c in nome:
            if c not in mau_elementos:
                if tag == '':
                    tag = nome.replace(str(c), '_')
                else:
                    tag = tag.replace(str(c), '_')
        if 'Dub' in nome or 'DUB' in nome or 'dub' in nome:
            idioma = ' #DUB'
        else:
            idioma = ' #LEG'
        descriçao = (
            f'     ✅{nome}\n'
            f'{"_" * (len(nome) + 5)}\n\n'
            f'#{tag[:24].replace("__", "_")}..\n'
            f'🎞 Episodios - {len(magnet2[0])}   |   '
            f'🇧🇷{idioma}'
        )
        # print(descriçao)
        botao_dict['nome'] = f'{nome[:8]}'
        botao_dict['link'] = f'{link}'
    else:
        for d in magnet2[0]:
            try:
                nome1 = str(d.text)
                if len(nome1) >= 3:
                    episodio = nome1[nome1.find('- ') + 2:]
                    num = episodio.find('- ')
                    if num != -1:
                        episodio = episodio[:num]
                    link = d['href']
                    print('>>', episodio)
                    botao_dict = {}
                    site = requests.get(link, headers=hesders)
                    soup = BeautifulSoup(site.content, 'html.parser')
                    magnet2 = soup.find_all('div', id='div_video')

                    for j in magnet2[0]:

                        try:
                            try:
                                link2 = j.video['data-video-src']
                            except:
                                pass
                                link2 = j.iframe['src']
                        except:
                            pass
                        else:
                            tratar_link = requests.get(link2)
                            links = str(tratar_link.text)
                            link3 = link2
                            if len(links) < 500:
                                inicio = links.find('http', 150)
                                if inicio <= -1:
                                    if len(links) <= 160:
                                        inicio = links.find('http')
                                    else:
                                        inicio = links.find('http', 30)
                                fim = links.find('label', inicio)
                                link3 = links[inicio:fim - 3].replace('\/', '/')

                            for c in nome:
                                if c not in mau_elementos:
                                    if tag == '':
                                        tag = nome.replace(str(c), '_')
                                    else:
                                        tag = tag.replace(str(c), '_')
                            if 'Dub' in nome or 'DUB' in nome or 'dub' in nome:
                                idioma = ' #DUB'
                            else:
                                idioma = ' #LEG'
                            descriçao = (
                                         f'     ✅{nome}\n'
                                         f'{"_" * (len(nome) + 5)}\n\n'
                                         f'#{tag[:24].replace("__", "_")}..\n'
                                         f'🎞{episodio.replace("o", "os")}   |   '
                                         f'🇧🇷{idioma}'
                                         )
                            # print(descriçao)
                            print(link3)
                            botao_dict['nome'] = f'{episodio}'
                            botao_dict['link'] = f'{link3}'
                            lista_botao.append(botao_dict)



            except:
                pass

    # for n, it in enumerate(botao_dict):
    #     print(n, it)
    #     print(botao_dict[it])
    #     markup.row(InlineKeyboardButton(it,
    #                                     web_app=WebAppInfo(botao_dict[it])))
    #     markup.add()
    # botao2 = quick_markup(botao_dict, row_width=3)
    # print(descriçao)

    lista.append(descriçao)
    lista.append(imagem)
    lista2.append(lista)
    lista2.append(lista_botao)

    cont += 1
    return lista2



if __name__ == '__main__':
    pesquisas('tensei')
#     enviar('https://animefire.plus/animes/naruto-shippuuden-todos-os-episodios')
#     lista2 = enviar('https://animefire.plus/animes/overlord-ii-dublado-todos-os-episodios')
#     botao2 = lista2[1]
#     descriçao, imagem = lista2[0]
#     print(botao2)


def botao(texto,    link):
    botao2 = InlineKeyboardMarkup(row_width=7)
    from telebot.util import quick_markup

    botao2 = quick_markup({

        texto: {'url': link},

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

def back_keyboard(lista):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(lista['nome'],
                                    web_app=WebAppInfo(lista["link"])))
    return markup
    # return InlineKeyboardMarkup(
    #     keyboard=[
    #         [
    #             types.InlineKeyboardButton(
    #                 lista[num]['nome'],
    #                 web_app=WebAppInfo(lista[num]["link"])
    #             )
    #         ]
    #         for num, product in enumerate(lista)
    #     ], row_width=7
    # )


def enviar2(link):
    descriçao = ''
    tag = ''
    hesders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}
    site = requests.get(link, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='sub_animepage_img')
    lista2 = []
    for d in magnet2[0]:
        try:
            nome = d['alt']
            imagem = d['data-src']
            print(imagem, '\n',
                  nome)
        except:
            pass
    site = requests.get(link, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='div_video_list')
    cont = 0
    lista = []
    botao_dict = {}
    if len(magnet2[0]) > 42:
        for c in nome:
            if c not in mau_elementos:
                if tag == '':
                    tag = nome.replace(str(c), '_')
                else:
                    tag = tag.replace(str(c), '_')
        if 'Dub' in nome or 'DUB' in nome or 'dub' in nome:
            idioma = ' #DUB'
        else:
            idioma = ' #LEG'
        descriçao = (
            f'     ✅{nome}\n'
            f'{"_" * (len(nome) + 5)}\n\n'
            f'#{tag[:24].replace("__", "_")}..\n'
            f'🎞 Episodios - {len(magnet2[0])}   |   '
            f'🇧🇷{idioma}'
        )
        # print(descriçao)
        botao_dict[f'{nome[:8]}'] = {'url': link}
    else:
        for d in magnet2[0]:
            try:
                nome1 = str(d.text)
                if len(nome1) >= 3:
                    episodio = nome1[nome1.find('- ') + 2:]
                    num = episodio.find('- ')
                    if num != -1:
                        episodio = episodio[:num]
                    link = d['href']
                    print('>>', episodio)
                    site = requests.get(link, headers=hesders)
                    soup = BeautifulSoup(site.content, 'html.parser')
                    magnet2 = soup.find_all('div', id='div_video')

                    for j in magnet2[0]:

                        try:
                            try:
                                link2 = j.video['data-video-src']
                            except:
                                pass
                                link2 = j.iframe['src']
                        except:
                            pass
                        else:
                            tratar_link = requests.get(link2)
                            links = str(tratar_link.text)
                            link3 = link2
                            if len(links) < 500:
                                inicio = links.find('http', 150)
                                if inicio <= -1:
                                    if len(links) <= 160:
                                        inicio = links.find('http')
                                    else:
                                        inicio = links.find('http', 30)
                                fim = links.find('label', inicio)
                                link3 = links[inicio:fim - 3].replace('\/', '/')

                            for c in nome:
                                if c not in mau_elementos:
                                    if tag == '':
                                        tag = nome.replace(str(c), '_')
                                    else:
                                        tag = tag.replace(str(c), '_')
                            if 'Dub' in nome or 'DUB' in nome or 'dub' in nome:
                                idioma = ' #DUB'
                            else:
                                idioma = ' #LEG'
                            descriçao = (
                                         f'     ✅{nome}\n'
                                         f'{"_" * (len(nome) + 5)}\n\n'
                                         f'#{tag[:24].replace("__", "_")}..\n'
                                         f'🎞{episodio.replace("o", "os")}   |   '
                                         f'🇧🇷{idioma}'
                                         )
                            # print(descriçao)
                            print(link3)
                            botao_dict[f'{episodio}'] = {'url': link3}

            except:
                pass
    botao2 = quick_markup(botao_dict, row_width=3)
    print(descriçao)
    lista.append(descriçao)
    lista.append(imagem)
    lista2.append(lista)
    lista2.append(botao2)
    cont += 1
    return lista2