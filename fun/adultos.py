import time

import anyio
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from telebot import formatting

from fun.arquivos_texto import abrir_reg, registro
from fun.solicitacoes import hesders, bot2, bot1
from keyboards import botao

tradutor = GoogleTranslator(source="en", target="portuguese")


async def xxx():
    page_num = int(abrir_reg('page_num_xxx'))
    while True:

        chat = -1002086116283

        if page_num == 0:
            page = f'https://m.tnaflix.com'
        else:
            page = f'https://www.tnaflix.com/featured/{page_num}'
        print('>> ', page)
        site = requests.get(page, headers=hesders)
        soup = BeautifulSoup(site.content, 'html.parser')
        magnet = soup.find_all('li')
        for div in magnet:
            try:
                page2 = div['data-vid']
            except:
                pass
            else:
                try:
                    titulo = tradutor.translate(str(div['data-name']))
                    imagem = div['data-trailer']
                    page2 = page + div.a['href']
                    try:
                        reg = abrir_reg('xxx')
                    except:
                        registro(f'{titulo}', 'xxx', 'nao')
                        reg = abrir_reg('xxx')
                    print(page2)
                except:
                    pass
                else:
                    print(titulo)
                    if titulo not in reg:
                        site2 = requests.get(page2, headers=hesders)
                        soup = BeautifulSoup(site2.content, 'html.parser')
                        magnet = soup.find_all('a', class_='video-link-detailed no_ajax')
                        tags = []
                        for f in magnet:
                            try:
                                texto = str(f.text)
                            except:
                                pass
                            else:
                                if texto not in '':
                                    tags.append(tradutor.translate(texto.strip().replace(' ', '_')))
                        tags = str(tags).replace("'", '').replace(', ', '  #').replace('[', '#').replace(']', '')

                        site2 = requests.get(page2, headers=hesders)
                        soup = BeautifulSoup(site2.content, 'html.parser')
                        magnet = soup.find_all('meta', itemprop='embedUrl')
                        page3 = magnet[0]['content']

                        site3 = requests.get(page3, headers=hesders)
                        soup = BeautifulSoup(site3.content, 'html.parser')
                        magnet = soup.find_all('script', type='text/javascript')
                        d = magnet[0]
                        num = str(d).find('config')
                        nun2 = str(d).find('"', num + 20)
                        page4 = 'https:' + str(d)[num + 10:nun2]
                        print(page4)
                        site4 = requests.get(page4, headers=hesders, verify=False)
                        link = str(site4.text)
                        num = link.rfind(']]></videoLink>')
                        link = link[:num]
                        nun2 = link.rfind('A[') + 2
                        link = 'https:' + link[nun2:].replace('https:', '')
                        print(link)
                        if page_num % 2 == 0:
                            bot2.send_video(chat, imagem, caption=formatting.mbold(f'❇️ {titulo}\n\n'
                                                                                   f'{tags}'),
                                            parse_mode='MarkdownV2',
                                            reply_markup=botao('Assistir', link))
                        else:
                            bot1.send_video(chat, imagem, caption=formatting.mbold(f'❇️ {titulo}\n\n'
                                                                                   f'{tags}'),
                                            parse_mode='MarkdownV2',
                                            reply_markup=botao('Assistir', link))
                        registro(f'{titulo}', 'xxx', 'nao')
                        await anyio.sleep(10)

                    else:
                        print('ja foi !')
        page_num += 1
        registro(page_num, 'page_num_xxx')
