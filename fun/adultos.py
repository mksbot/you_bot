import time

import anyio
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from telebot import formatting, types

from fun.arquivos_texto import abrir_reg, registro
from fun.solicitacoes import hesders, bot2, bot1
from keyboards import botao

tradutor = GoogleTranslator(source="en", target="portuguese")
# page_num = int(abrir_reg('page_num_xxx'))
page_num = 0
chat = -1002086116283


def inline_xxx(texto):
    page = f'https://www.pornomineiro.com/?s={texto.replace(".p ", "").replace(" ", "-")}'
    print(page)
    hesders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}

    site = requests.get(page, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('section', class_='pst-cn clma06c04d03')
    lista_inline = []
    for v in magnet2[:10]:
        lista_inline2 = []
        link = v.figure.a['href']
        titulo = tradutor.translate(v.figure.img['alt'])
        imagem = v.figure.img['src']
        lista_inline2.append(titulo)
        lista_inline2.append(str(imagem))
        lista_inline2.append(link)
        lista_inline.append(lista_inline2)
    # if len(magnet2[0]) - 3 >= 46:
    #     page = f'https://animefire.plus/pesquisar/{str(texto).replace(" ", "-")}/2'
    #     site = requests.get(page, headers=hesders)
    #     soup = BeautifulSoup(site.content, 'html.parser')
    #     magnet2 = soup.find_all('div', class_='row ml-1 mr-1')
    #     for v in magnet2[0]:
    #         try:
    #             nome = str(v['title']).replace('- Todos os Episódios', '')
    #         except:
    #             pass
    #         else:
    #             lista_inline2 = []
    #             link = v.a['href']
    #             imagem = v.a.img['data-src']
    #
    #             lista_inline2.append(nome)
    #             lista_inline2.append(imagem)
    #             lista_inline2.append(link)
    #             lista_inline.append(lista_inline2)

    pesquisar = lista_inline
    itens = []
    for n, v in enumerate(pesquisar):
        titulo, thumbnail_url, url = pesquisar[n]
        print(titulo)
        itens.append(types.InlineQueryResultArticle(f'{n}', f'{titulo}',
                                                    types.InputTextMessageContent(url),
                                                    thumbnail_url=f'{thumbnail_url}',thumbnail_width='600'))

    return itens


def xxx(page):
    print('>> ', page)
    site = requests.get(page, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet = soup.find_all('section', class_='pst-cn clma06c04d03')
    for it in magnet:
        page2 = it.figure.a['href']
        titulo = it.figure.img['alt']
        imagem = it.figure.img['src']
        print(titulo)
        print(imagem)
        xxx_player(page2, titulo, imagem)


def xxx_player(page2, titulo, imagem):
    print(titulo)
    try:
        reg = abrir_reg('xxx')
    except:
        registro(f'{titulo}', 'xxx', 'nao')
        reg = abrir_reg('xxx')
    if titulo not in reg:
        site2 = requests.get(page2, headers=hesders)
        soup = BeautifulSoup(site2.content, 'html.parser')
        magnet = soup.find_all('p')
        tags = []
        link = magnet[1].iframe['src']
        for t in magnet[3]:
            tags.append(tradutor.translate(t.text.strip().replace(' ', '_')))
        for t in magnet[4]:
            tags.append(tradutor.translate(t.text.strip().replace(' ', '_')))

        tags = str(tags).replace(
            "'", '').replace(
            ", ", ' #').replace(
            '[', '#').replace(
            ']', '').replace(
            '# ', '').replace(
            '#Categorias: ', '').replace(
            '#Atriz_Pornô: ', '')
        print(tags)

        print(link)

        bot2.send_photo(chat, imagem, caption=formatting.mbold(f'❇️ {titulo}\n\n'
                                                                   f'{tags}'),
                            parse_mode='MarkdownV2',
                            reply_markup=botao('Assistir', link))

        # bot1.send_video(chat, imagem, caption=formatting.mbold(f'❇️ {titulo}\n\n'
        #                                                            f'{tags}'),
        #                     parse_mode='MarkdownV2',
        #                     reply_markup=botao('Assistir', link))
        registro(f'{titulo}', 'xxx', 'nao')
        time.sleep(5)

    else:
        print('ja foi !')
    # page_num += 1
    # registro(page_num, 'page_num_xxx')


if __name__ == '__main__':
    inline_xxx('.PN')
