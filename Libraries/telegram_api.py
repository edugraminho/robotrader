from telethon.sync import TelegramClient
from telethon import functions, events, types
from Variables.config import *
from Libraries.utils import *
from Libraries.logger import get_logger

import time
import socks

"""
Para conseguir logar na sessao tem q entrar em https://my.telegram.org.
Pegar o ID e HASH 
Copiar o arquivo gerado e jogar no repo do robo

45.91.10.76:30001

"""
logger = get_logger(__name__)

def connect():
    logger.info("Iniciando conexao Telegram")
    try:
        proxy = (socks.SOCKS5, "45.239.152.141", "3001")
        client = TelegramClient(proxy=proxy, session=f'{DATA_DIRECTORY}/session_name', api_id=API_ID, api_hash=API_HASH)
        client.connect()

        return client
    except Exception as e:
        logger.error(f"Erro ao conectar Telegram: {e}")
        time.sleep(2)
        connect()


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
                messages = client.get_messages(chat, limit=5)
                for message in messages:
                    check_csv = check_index_repeated(message.id)
                    if check_csv:
                        # reply_to = check_reply_to(message)
                        # print(f"***************{message.id}*******************")
                        # print(message.message)
                        # print("***************************************")
                        insert_csv(message.message, message.id)

    except Exception as e:
        logger.error(f"Error get_messages_group: {e}")
        pass
