from pathlib import Path, PurePath
import os
from datetime import datetime


# ==================== API BINANCE ====================
QNT_CRYPTOS_TO_PURCHASE = 30 #o maximo de cryptos a serem negociadas, total / pelo saldo
PERCENTAGE_STOP = 2
LEVERAGE = 20

LIST_TARGETS_TAKE_PROFITS = [2, 4, 6]

# API_KEY EDU
API_KEY = "m8g5mtYnftzWUTYAGro7U77lE42ky7KRk7ylNGAmb8CtLVSOuqp7G5PwTLHjll45"
API_SECRET = "Vx2FRCexMsI8Lz3OG6WqoleIJjUY8ScuoIHfBt2XgJpYAss5f2bv1clerDvZCoA5"
# ======================================================


# ==================== API TELEGRAM ====================
API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'

MESSAGES_LIMIT = 10
# ======================================================


# ==================== MONGO-DB ====================
DB_USER = 'robotraderUser'
DB_PASSWORD = 'qTyoyZka0dsi1UwI'
CLUSTER = 'cluster0'
URI = f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER}.94tddj0.mongodb.net/?retryWrites=true&w=majority'
# ======================================================


# ====================== DIRETÓRIOS LOCAIS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
NOW = datetime.now().strftime("%d/%m %H:%M")
DATA_DIRECTORY = os.path.join(ROOT, "Data")
# ===============================================================
