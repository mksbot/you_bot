import asyncio
import random
import sys
import subprocess
import os
from time import sleep
import requests
import telebot
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from telebot import formatting
from telebot.util import quick_markup
from fun.arquivos_texto import abrir_reg, registro
from keyboards import botao

cor = [Fore.LIGHTYELLOW_EX + Back.BLACK, Fore.LIGHTBLUE_EX + Back.BLACK, Fore.GREEN + Back.BLACK,
       Fore.MAGENTA + Back.BLACK, Back.BLACK, Fore.LIGHTRED_EX + Back.BLACK]
r = [Fore.RESET, Style.RESET_ALL, Back.RESET]
API_TOKEN = ['6812826133:AAHTh_ZzbOSXeKjAedxwpPKJMeuMt6AT-o8',
             '6859056897:AAFAhdg80DyiYjBX3lIKBzZ-xWaRqDDQGQ8']
hesders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}
bot1 = telebot.TeleBot(API_TOKEN[0])
bot2 = telebot.TeleBot(API_TOKEN[1])


async def hentais():
    for w in range(0, int(abrir_reg('page_num'))):
        page_num = int(abrir_reg('page_num'))
        chat = -1002073463326
        if page_num == 0:
            page = f'https://animeshentai.biz/hentai/'
        else:
            page = f'https://animeshentai.biz/hentai/page/{page_num}/'
        print('>> ',page)
        site = requests.get(page, headers=hesders)
        soup = BeautifulSoup(site.content, 'html.parser')
        magnet = soup.find_all('div', class_='animation-2 items')
        for div in magnet[0]:
            if 'http' in str(div.div.a['href']):
                page2 = div.div.a['href']
            else:
                page2 = f'https://animeshentai.biz{div.div.a["href"]}'
            print(page2)
            site = requests.get(page2, headers=hesders)
            soup = BeautifulSoup(site.content, 'html.parser')
            magnet2 = soup.find('div', class_='sgeneros')
            tags = []
            for t in magnet2:
                tags.append(f'{t.text}'.replace(' ', "_"))
            tags = str(tags[1:]).replace('[', '#').replace(']', '').replace(', ', ' #').replace("'", '')
            soup = BeautifulSoup(site.content, 'html.parser')
            magnet2 = soup.find_all('div', class_='content')
            for div2 in magnet2:
                try:
                    capa = div2.img['src']
                except:
                    pass
                else:
                    titulo = div2.img['alt']
                    sinopse = str(div2.p.text)
                    print(titulo)
                    try:
                        reg = abrir_reg('hentais')
                    except:
                        registro(titulo, 'hentais', 'nao')
                        reg = abrir_reg('hentais')

                    if titulo not in reg:
                        epsodios = {}
                        cont = 1
                        for c in div2:
                            try:
                                eps = c.ul
                            except:
                                pass
                            else:
                                if eps:
                                    for ep in eps:
                                        if ep.div.a:
                                            imagem = ep.div.a.img['src']
                                            player = ep.div.a['href']

                                            page3 = player
                                            site = requests.get(page3, headers=hesders)
                                            soup = BeautifulSoup(site.content, 'html.parser')
                                            magnet3 = soup.find_all('iframe', class_='metaframe rptss')
                                            link = magnet3[0]['src']

                                            epsodios[f'Episodio {cont}'] = [imagem, link]
                                            cont += 1

                        if page_num % 2 == 0:
                            marckup = bot1.send_photo(chat, capa, caption=formatting.format_text(
                                formatting.mcode(f"{titulo}").upper(),
                                formatting.escape_markdown(f'SINOPSE: {sinopse}'),
                                formatting.mbold(tags),
                                separator="\n\n"
                            ),
                                                      parse_mode='MarkdownV2'
                                                      )
                            for chave in epsodios:
                                ep = chave
                                imagem, link = epsodios[chave]
                                print(imagem)
                                print(link)
                                print(ep)

                                bot1.send_photo(chat, photo=imagem, reply_markup=botao(ep, link),
                                                reply_to_message_id=marckup.id)
                                registro(titulo, 'hentais', 'nao')

                        else:
                            marckup = bot2.send_photo(chat, capa, caption=formatting.format_text(
                                formatting.mcode(f"{titulo}").upper(),
                                formatting.escape_markdown(f'SINOPSE: {sinopse[:290]}..'),
                                formatting.mbold(tags),
                                separator="\n\n"
                            ),
                                                      parse_mode='MarkdownV2'
                                                      )

                            for chave in epsodios:
                                ep = chave
                                imagem, link = epsodios[chave]
                                print(imagem)
                                print(link)
                                print(ep)

                                bot2.send_photo(chat, photo=imagem, reply_markup=botao(ep, link),
                                                reply_to_message_id=marckup.id)
                                registro(titulo, 'hentais', 'nao')

                        await asyncio.sleep(random.randint(0, 500))
                    else:
                        print('Ja foi!!')
        page_num -= 1
        registro(page_num, 'page_num')


async def noticias():
    chat_testes = -1002073463326
    chat = -1002000136655
    page = f'https://vocesabianime.com/'
    print(page)
    site = requests.get(page, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='ultp-block-items-wrap ultp-block-row ultp-pg1a-style1 ultp-block-column-3 '
                                          'ultp-layout1')

    for c in magnet2[0]:
        autor = c.next.span.a.text
        categoria = str(c.next.next.div.text)
        imagem = c.a.img['src']
        link = c.a['href']
        titulo = c.a.img['alt']
        if autor not in 'Você Sabia Anime':
            try:
                reg = abrir_reg('noticias')
            except:
                registro(titulo, 'noticias', 'nao')
                reg = abrir_reg('noticias')

            if titulo not in reg:
                await asyncio.sleep(2)
                descriçao = (f'✨Novidades Otaku✨'
                             f'\n\n👁‍🗨 {titulo}\n\n'
                             f'#{categoria.replace(" ", "_")}')
                print(f'Enviando: {titulo}')
                bot2.send_photo(chat, imagem, caption=descriçao, reply_markup=botao('Saiba Mais', link))
                registro(titulo, 'noticias', 'nao')


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
    soup = BeautifulSoup(site.content, 'html.parser')
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
                     f'{"_" * 25}\n\n'
                     f'#{tag[:24].replace("__", "_")}..\n'
                     f'🎞{episodio}   |   '
                     f'🇧🇷 #{idioma}'
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
                    soup = BeautifulSoup(site.content, 'html.parser')
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
                    print(nome)



                except:
                    pass
        else:

            pass

    print(f'>> Encontrei : [{len(lista)}] Novos Animes!!')
    # ANIMES DUBLADO
    page = f'https://animefire.plus'
    print(page)
    site = requests.get(page, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='row ml-1 mr-1 mr-md-2')

    for v in magnet2[0]:
        lista2 = []
        informaçoes = str(v.text).replace('     ', '>')
        num = informaçoes.find('- E')
        episodio = informaçoes[num + 1:informaçoes.find('>', num)]
        nome = informaçoes[:num].replace(">", " ").upper()

        mau_elementos = (
            "a,b,c,ç,Ç,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,"
            "Y,Z,À,Á,Â,Ä,Å,Ã,Æ,Ç,É,È,Ê,Ë,Í,Ì,Î,Ï,Ñ,Ó,Ò,Ô,Ö,Ø,Õ,O,E,Ú,Ù,Û,Ü,Ý,Y à,á,â,ä,å,ã,æ,ç,é,è,ê,ë,í,ì,î,ï,ñ,ó,ò,"
            "ô,ö,ø,õ,o,e,ú,ù,û,ü,ý,y".replace(',', ' ').split())
        tag = ''
        if 'Dub' in nome or 'DUB' in nome or 'dub' in nome:
            idioma = f'#DUB'
        else:
            idioma = f'#LEG'
        for c in nome:
            if c not in mau_elementos:
                if tag == '':
                    tag = nome.replace(str(c), '_')
                else:
                    tag = tag.replace(str(c), '_')
        descriçao = (f'> Fonte--2'
                     f'\n\n'
                     f'     ✅{nome}\n'
                     f'{"_" * 25}\n\n'
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

            try:
                link = v.a['href']
                site = requests.get(link, headers=hesders)
                soup = BeautifulSoup(site.content, 'html.parser')
                magnet2 = soup.find_all('div', id='div_video', )
                for j in magnet2[0]:
                    try:
                        link2 = j.video['data-video-src']
                    except:
                        pass

                tratar_link = requests.get(link2)
                links = str(tratar_link.text)

                inicio = links.find('http', 150)
                if inicio <= -1:
                    if len(links) <= 160:
                        inicio = links.find('http')
                    else:
                        inicio = links.find('http', 30)
                fim = links.find('label', inicio)
                link3 = links[inicio:fim - 3].replace('\/', '/')
                imagem = v.img['data-src']

                botao = quick_markup({

                    'ASSISTIR | BAIXAR': {'url': link3},

                }, row_width=2)
                lista2.append(botao)
                lista2.append(imagem)
                lista2.append(f'{nome + episodio}')
                lista.append(lista2)
                print(nome)
            except:
                pass
        else:
            pass

    print(f'>> Encontrei : [{len(lista)}] Novos Animes!!')
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


def restart():
    # Run the git pull command

    result = subprocess.run(["git", "pull"], stdout=subprocess.PIPE)
    # Check the exit code of the command
    if result.returncode != 0:
        print("Error: Git pull failed with exit code {}".format(result.returncode))
    else:
        print("Success: Git pull was executed successfully.")
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    os.execv(sys.executable, ['python'] + sys.argv)


def pergunta(text):
    while True:
        try:
            cele = int(input(f"\n{text}: "))
        except:
            print(cor[5], '\n Digito Incorreto', r[1])
        else:
            print(cor[2], f' >> OK....{r[1]}\n {"-" * 65}\n')
            return cele
            break


def pergunta_testo(text):
    while True:
        try:
            cele = (input(f"\n{text}: "))
        except:
            print(f'\n{cor[5]}  Digito Incorreto', r[1])
            print(f'\n{cor[2]} >> OK....{r[1]}\n {"-" * 65}\n')
            return cele
            break


def textos_prin(t1, t2):
    if len(t1) > len(t2):
        tamanho = len(t1)
    else:
        tamanho = len(t2)
    print(
        f'\n {"-" * 65}\n\n{cor[0]} >> Transferindo midias <<{r[1]}\n {"-" * 65}\n DE: {t1}\n\n PARA: {t2}\n {"-" * 65}\n')
