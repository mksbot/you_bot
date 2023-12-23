from telebot.async_telebot import AsyncTeleBot
from telebot import formatting


API_TOKEN = ['6812826133:AAHTh_ZzbOSXeKjAedxwpPKJMeuMt6AT-o8',
             '6859056897:AAFAhdg80DyiYjBX3lIKBzZ-xWaRqDDQGQ8']
hesders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}
bot = AsyncTeleBot(API_TOKEN[0])


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(
        message.chat.id,
        # function which connects all strings
        formatting.format_text(
            formatting.mbold(message.from_user.first_name),
            formatting.mitalic(message.from_user.first_name),
            formatting.munderline(message.from_user.first_name),
            formatting.mstrikethrough(message.from_user.first_name),
            formatting.mcode(message.from_user.first_name),
            separator=" " # separator separates all strings
        ),
        parse_mode='MarkdownV2'
    )

    # just a bold text using markdownv2
    await bot.send_message(
        message.chat.id,
        formatting.mbold(message.from_user.first_name),
        parse_mode='MarkdownV2'
    )

    # html
    await bot.send_message(
        message.chat.id,
        formatting.format_text(
            formatting.hbold(message.from_user.first_name),
            formatting.hitalic(message.from_user.first_name),
            formatting.hunderline(message.from_user.first_name),
            formatting.hstrikethrough(message.from_user.first_name),
            formatting.hcode(message.from_user.first_name),
            # hide_link is only for html
            formatting.hide_link('https://telegra.ph/file/c158e3a6e2a26a160b253.jpg'),
            separator=" "
        ),
        parse_mode='HTML'
    )

    # just a bold text in html
    await bot.send_message(
        message.chat.id,
        formatting.hcode(message.from_user.first_name),
        parse_mode='HTML'
    )

import asyncio
asyncio.run(bot.polling())