import os

from colorama import Fore, Back, Style
from pytube import YouTube

cor = [Fore.LIGHTYELLOW_EX + Back.BLACK, Fore.LIGHTBLUE_EX + Back.BLACK, Fore.GREEN + Back.BLACK,
       Fore.MAGENTA + Back.BLACK, Back.BLACK, Fore.LIGHTRED_EX + Back.BLACK]
r = [Fore.RESET, Style.RESET_ALL, Back.RESET]

def baixarmp3(link, itag):
    yt = YouTube(link)
    yt.streams.filter(only_audio=True)
    video = yt.streams.get_by_itag(itag)
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    nome = str(new_file[new_file.find('bot3') + 6:])
    try:
        os.rename(out_file, new_file)
    except:
        pass
    print(yt.title + " Baixado com sucesso")
    return str(nome)

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

def textos_prin(t1,t2):
    if len(t1) > len(t2):
        tamanho = len(t1)
    else:
        tamanho = len(t2)
    print(f'\n {"-" * 65}\n\n{cor[0]} >> Transferindo midias <<{r[1]}\n {"-" * 65}\n DE: {t1}\n\n PARA: {t2}\n {"-" * 65}\n')
