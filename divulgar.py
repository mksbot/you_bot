import asyncio
import os
from fun import arquivos_texto
from time import sleep
from random import randint
from telethon import TelegramClient, events, Button
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Use your own values from my.telegram.org
api_id = 22217845
api_hash = '419b473e8797968bb157b29bffa1ee45'
client = TelegramClient('upalto', api_id, api_hash)

lista = [c for c in range(0, 1010)]
async def compartilhar():
    async for dialog in client.iter_dialogs():

        if "link" in dialog.name or "Link" in dialog.name or "LINK" in dialog.name:
            if 'Parceiros' not in dialog.name:
                print(dialog.name)
                await client.send_message(dialog.id, message='Animes hentai 👇✨\n'
                                                             'https://t.me/+YQcQI3jNhvA5MWFh\n\n'
                                                             'Grupo de animes👇✨\n'
                                                             'https://t.me/+eGIsvENJighiNGNh\n\n'
                                                             'Crupo novo 👇✨\n'
                                                             'https://t.me/+Q14A4CSfZFo5ZWI5'
                                          )
                await asyncio.sleep(1)


async def iniciar():
    for c in lista:
        with client:
            client.loop.run_until_complete(compartilhar())
        await asyncio.sleep(3600)
