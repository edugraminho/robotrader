import asyncio
from telethon.sync import TelegramClient
from telethon import functions, events, types
from Variables.config import *


"""
Para conseguir logar na sessao tem q entrar em https://my.telegram.org.
Pegar o ID e HASH 
Copiar o arquivo gerado e jogar no repo do robo
"""

API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'

def main():
  with TelegramClient(f'{DATA_DIRECTORY}/telegram_session', API_ID, API_HASH) as client:

    result = client(functions.messages.GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=types.InputPeerEmpty(),
        limit=500,
        hash=-0,
    ))

    title = "Brazza Scalping Vip"
    for chat in result.chats:
        if chat.title == title:
            messages = client.get_messages(chat, limit=100)
            for message in messages:
                print(50*'*')
                print(message.id)
                print(message.message)
                print(message.reply_to)
                print(message.date)
                print(50*'*')
    client.disconnect()


def get_messages_group(client):
    try:

        result = client(functions.messages.GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=types.InputPeerEmpty(),
            limit=500,
            hash=-0,
        ))

        title = "Brazza Scalping Vip"
        for chat in result.chats:
            if chat.title == title:
                messages = client.get_messages(chat, limit=100)
                for message in messages:
                    # insert_csv(message.message, message.id, index)
                    print(50*'*')
                    print(message.id)
                    print(message.message)
                    print(message.reply_to)
                    print(message.date)
                    print(50*'*')
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(get_messages_group())
        # loop.close()
        
    except Exception as e:
        print(f"Error: {e}")

def main1():
    client = TelegramClient(f'{DATA_DIRECTORY}/telegram_session', API_ID, API_HASH)
    client.connect()
    get_messages_group(client)

main1()