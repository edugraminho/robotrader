import asyncio
from telethon.sync import TelegramClient
from telethon import functions, events, types
from robot.api import logger

from Variables.config import *
from Libraries.utils import insert_csv


"""
  Para conseguir logar na sessao tem q entrar em https://my.telegram.org.
  Pegar o ID e HASH 
  Copiar o arquivo gerado e jogar no repo do robo
  (arquivo api-telegram nos Projetos)
"""

def as_get_messages_group(client):
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
                for index, message in enumerate(messages):
                    insert_csv(message.message, message.id, index)

                    #manter robo sempre ligado capturando as msgs
                    
                    print(50*'*')
                    print(message.id)
                    print(message.message)
                    print(message.reply_to)
                    logger.info(message.date)
                    print(50*'*')

        
    except Exception as e:
        logger.error(f"Error: {e}")

def get_messages_group():
    client = TelegramClient('session_name', API_ID, API_HASH)
    client.connect()
    as_get_messages_group(client)



