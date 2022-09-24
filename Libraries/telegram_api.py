from telethon.sync import TelegramClient
from telethon import functions, events, types
from Variables.config import *
from Libraries.utils import *

import time
import socks
"""
Para conseguir logar na sessao tem q entrar em https://my.telegram.org.
Pegar o ID e HASH 
Copiar o arquivo gerado e jogar no repo do robo


45.91.10.76:30001

"""

API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'
def connect():
    try:
        proxy = (socks.SOCKS5, "45.239.152.141", "3001")
        client = TelegramClient(proxy=proxy, session=f'{DATA_DIRECTORY}/session_name', api_id=API_ID, api_hash=API_HASH)
        client.connect()

        return client
    except:
        print("Tentando conectar-se ao Telegram de novo")
        time.sleep(2)
        connect()




def get_messages_group(client):
    try:
        # proxy = (socks.SOCKS5, "45.239.152.141", "3001")
        # client = TelegramClient(proxy=proxy, session=f'{DATA_DIRECTORY}/session_name', api_id=API_ID, api_hash=API_HASH)
        # client.connect()


        result = client(functions.messages.GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=types.InputPeerEmpty(),
            limit=500,
            hash=-0,
        ))
        print("Buscando Mensagens")
        title = "Brazza Scalping Vip"
        for chat in result.chats:
            if chat.title == title:
                messages = client.get_messages(chat, limit=1)
                for message in messages:
                    check_csv = check_its_repeated(message.id)
                    if check_csv:
                        res = insert_csv(message.message, message.date, message.id)
                        if res:
                            print(f"Inserindo Spot no csv, ID: {message.id}")

                    # time.sleep(3)


    except Exception as e:
        print(f"Error: {e}")
        raise e



