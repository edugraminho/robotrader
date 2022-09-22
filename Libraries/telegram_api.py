from telethon.sync import TelegramClient
from telethon import functions, events, types
from Variables.config import *
from Libraries.utils import insert_csv, last_index

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


def get_messages_group():
    try:
        proxy = (socks.SOCKS5, "45.239.152.141", "3001")
        print('proxy', proxy)
        client = TelegramClient(proxy=proxy, session=f'{DATA_DIRECTORY}/session_name', api_id=API_ID, api_hash=API_HASH)
        client.connect()

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
                while True:
                    messages = client.get_messages(chat, limit=10)
                    for message in messages:
                        last = last_index()
                        if last != int(message.id):
                            res = insert_csv(message.message, message.date, message.id)
                            if res:
                                print(50*'*')
                                print(message.id)
                                print(message.message)
                                if message.reply_to:
                                    print("reposta: ", message.reply_to.reply_to_msg_id)

                        time.sleep(10)

        
    except Exception as e:
        print(f"Error: {e}")
        raise e



