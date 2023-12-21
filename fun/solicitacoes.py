import os
from colorama import Fore, Back, Style


cor = [Fore.LIGHTYELLOW_EX + Back.BLACK, Fore.LIGHTBLUE_EX + Back.BLACK, Fore.GREEN + Back.BLACK,
       Fore.MAGENTA + Back.BLACK, Back.BLACK, Fore.LIGHTRED_EX + Back.BLACK]
r = [Fore.RESET, Style.RESET_ALL, Back.RESET]

def restart():
    import sys
    import subprocess
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

    import os
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

def textos_prin(t1,t2):
    if len(t1) > len(t2):
        tamanho = len(t1)
    else:
        tamanho = len(t2)
    print(f'\n {"-" * 65}\n\n{cor[0]} >> Transferindo midias <<{r[1]}\n {"-" * 65}\n DE: {t1}\n\n PARA: {t2}\n {"-" * 65}\n')
