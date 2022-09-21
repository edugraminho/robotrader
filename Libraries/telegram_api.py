from telethon.sync import TelegramClient
from telethon import functions, events, types
from Variables.config import *
from Libraries.utils import insert_csv


"""
Para conseguir logar na sessao tem q entrar em https://my.telegram.org.
Pegar o ID e HASH 
Copiar o arquivo gerado e jogar no repo do robo
"""

API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'


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
                messages = client.get_messages(chat, limit=10)
                for message in messages:
                    insert_csv(message.message, message.date, message.id)
                    print(50*'*')
                    print(message.id)
                    print(message.message)
                    if message.reply_to:
                        print(message.reply_to.reply_to_msg_id)
                    print(message.date.strftime("%d-%m %H:%M"))
                    print(50*'*')

        
    except Exception as e:
        print(f"Error: {e}")
        raise e

def connect_telegram():
    client = TelegramClient(f'{DATA_DIRECTORY}/session_name', API_ID, API_HASH)
    client.connect()
    get_messages_group(client)
