from pathlib import Path, PurePath
import os
from datetime import datetime


# ==================== API BINANCE ====================
QNT_CRYPTOS_TO_PURCHASE = 45 #o maximo de cryptos a serem negociadas, total / pelo saldo
PERCENTAGE_STOP = 2
LEVERAGE = 20

LIST_PERCENTAGE_TAKE_PROFITS = [2, 4, 6]


API_KEY = "L8vTV38sqckhCZCT403TlRqxZHSGuASm95QckB9y5Hmg6g1OUddff79Y1k9DGGLb"
API_SECRET = "X4TE8ehw2891qrLgT4iQSoFn6kwnQXy1V6ispA34cdWf0kq9PXP9Xa1d1EW880Nt"
# ======================================================


# ==================== API TELEGRAM ====================
API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'
# ======================================================


# ==================== MONGO-DB ====================
DB_USER = 'robotraderUser'
DB_PASSWORD = 'qTyoyZka0dsi1UwI'
STR_CONNECTION = f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.94tddj0.mongodb.net/?retryWrites=true&w=majority'
# ======================================================


# ====================== DIRETÓRIOS LOCAIS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
NOW = datetime.now().strftime("%d/%m %H:%M")
DATA_DIRECTORY = os.path.join(ROOT, "Data")
# ===============================================================
