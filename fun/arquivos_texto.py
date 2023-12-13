import json
import pickle
import random

import numpy as np


def registro(registrar, nome='arq01', nun=False):
    if nun:
        with open(f'{nome}.txt', 'w') as arquivo:
            arquivo.write(f'{registrar}')
            arquivo.close()

    else:
        lista = []
        try:
            add = abrir_reg(nome)
            print('abriu')
        except:
            print('nao abril')
            arquivo = open(f'{nome}.json', 'w')
            json.dump(registrar, arquivo)
            arquivo.close()
        else:
            for l in add:
                lista.append(l)
            for l2 in registrar:
                lista.append(l2)
            arquivo = open(f'{nome}.json', 'w')
            json.dump(lista, arquivo)
            arquivo.close()


def abrir_reg(nome="arq01", num=False):
    if num:
        with open(f'{nome}.txt') as arquivo:
            b = (arquivo.read())
            return b
    else:
        arquivo = open(f'{nome}.json', 'r')
        b = json.load(arquivo)
        arquivo.close()
        return b

