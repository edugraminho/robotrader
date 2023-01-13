from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from Variables.config import *
from Libraries.utils import *
from Libraries.logger import get_logger

import time
import python_socks

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
        proxy = (python_socks.ProxyType.SOCKS4, "149.154.167.50", 443)
        logger.info(proxy)
        # logger.info(f'{DATA_DIRECTORY}/session_name')
        client = TelegramClient(proxy=proxy, session=f'{DATA_DIRECTORY}/session_name.session', api_id=API_ID, api_hash=API_HASH)
        # logger.info(client.__dict__)

        # client.connect()

        return client
    except Exception as e:
        logger.error(f"Erro ao conectar Telegram: {e}")
        time.sleep(2)
        connect()


def get_messages_group():
    try:
        with TelegramClient(session=f'{DATA_DIRECTORY}/session_name.session', api_id=API_ID, api_hash=API_HASH) as client:

            result = client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=500,
                hash=-0,
            ))

            title = "Scalping_300%"
            for chat in result.chats:

                if chat.title == title:
                    messages = client.get_messages(chat, limit=10)
                    print(messages)
                    for message in messages:
                        check_csv = check_index_repeated(message.id)
                        if check_csv:
                            # reply_to = check_reply_to(message)
                            # print(f"***************{message.id}*******************")
                            # print(message.message)
                            # print("***************************************")
                            insert_csv(message.message, message.date, message.id)

        client.disconnect()
    except Exception as e:
        logger.error(f"Error get_messages_group: {e}")
        pass
