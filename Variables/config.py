from pathlib import Path, PurePath
import os
from datetime import datetime, timedelta


# ==================== API BINANCE ====================
QNT_CRYPTOS_TO_PURCHASE = 100 #o maximo de cryptos a serem negociadas, total / pelo saldo
PERCENTAGE_STOP = 2
LEVERAGE = 20

LIST_TARGETS_TAKE_PROFITS = [4, 7]

# API_KEY EDU
API_KEY = ""
API_SECRET = ""
# ======================================================


# ==================== API TELEGRAM ====================
API_ID = 
API_HASH = ''

MESSAGES_LIMIT = 5
# ======================================================


# ==================== MONGO-DB ====================
DB_USER = 'robotraderUser'
DB_PASSWORD = ''
CLUSTER = ''
URI = f''
DATA_TO_DELETE_OLD_DATA_MONGODB = datetime.now() - timedelta(days=3)


# ======================================================


# ====================== DIRETÓRIOS LOCAIS e DATAS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_DIRECTORY = os.path.join(ROOT, "Data")
NOW = datetime.now().strftime("%d/%m %H:%M")
CURRENT_DAY = datetime.now().strftime("%d/%m")
# ===============================================================
