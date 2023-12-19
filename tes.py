import random
import time

import requests
from bs4 import BeautifulSoup
from telebot.util import quick_markup

from fun.arquivos_texto import abrir_reg, registro
from main import bot2, bot1


def calendario_a():
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
        descriçao = (f'{"_" * (len(nome) + 10)}\n\n'
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

            print('>> JA FOI ENVIADO !!')
        # ANIMES DUBLADO
    page = f'https://animefire.plus'
    print(page)
    hesders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}
    site = requests.get(page, headers=hesders)
    soup = BeautifulSoup(site.content, 'html.parser')
    magnet2 = soup.find_all('div', class_='row ml-1 mr-1 mr-md-2')

    for v in magnet2[0]:
        lista2 = []
        informaçoes = str(v.text).replace('     ', '>')
        num = informaçoes.find('- E')
        episodio = informaçoes[num + 1:informaçoes.find('>', num)]
        nome = informaçoes[:num].replace(">", " ").upper()
        if 'Dub' in nome or 'DUB' in nome or 'dub' in nome:
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
            idioma = ' #DUB'
            descriçao = (f'{"_" * (len(nome) + 10)}\n\n'
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
                    print(links)
                    inicio = links.find('http', 150)
                    if inicio <= -1:
                        if len(links) <= 160:
                            inicio = links.find('http')
                        else:
                            inicio = links.find('http', 30)
                    fim = links.find('label', inicio)
                    link3 = links[inicio:fim - 3].replace('\/', '/')
                    imagem = v.img['data-src']
                    print(link3)
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

                print('>> JA FOI ENVIADO !!')
    lista.reverse()
    if f'{len(lista)}' not in '0':
        for num, it in enumerate(lista):
            descriçao, botao, imagem, nomer = lista[num]
            print(nomer)
            print('>> ENVIANDO !!')
            time.sleep(random.randint(0, 1))
            if num % 2 == 0:
                bot2.send_photo(chat, f'{imagem}', caption=f'{descriçao}', reply_markup=botao)
            else:
                bot1.send_photo(chat, f'{imagem}', caption=f'{descriçao}', reply_markup=botao)
            registro(f'{nomer}', 'animes', 'nao')


calendario_a()
