def registro(registrar, nome='arq01', substituir="sim"):
    if substituir == "sim":
        s = 'w'
    else:
        s = 'a'
    with open(f'{nome}.txt', f'{s}', encoding="utf-8") as arquivo:
        if s == 'w':
            arquivo.write(f'{registrar}')
        else:
            arquivo.write(f'{registrar}\n')
        arquivo.close()


def abrir_reg(nome="arq01"):
        with open(f'{nome}.txt',encoding="utf-8") as arquivo:
            b = (arquivo.read())
            return b


