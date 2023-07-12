from pathlib import Path, PurePath
import os
from datetime import datetime, timedelta


# ==================== API BINANCE ====================
QNT_CRYPTOS_TO_PURCHASE = 10 #o maximo de cryptos a serem negociadas, total / pelo saldo
PERCENTAGE_STOP = 2
LEVERAGE = 20

LIST_TARGETS_TAKE_PROFITS = [4, 7]

# API_KEY EDU
API_KEY = "KMd7eeFhDUElfn3bDZDbJKZtWJfFFtBXnC9cR18H6fy4t9kUsEIcggYuy8AVMd1p"
API_SECRET = "SJLOc00gCFdLNcq25YcPlkD6i9aozYWYmp1hvuyXQ6cLKCmbCWQRabqVE4t5N3tm"
# ======================================================


# ==================== API TELEGRAM ====================
API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'

MESSAGES_LIMIT = 5
# ======================================================


# ==================== MONGO-DB ====================
DB_USER = 'robotraderUser'
DB_PASSWORD = 'qTyoyZka0dsi1UwI'
CLUSTER = 'cluster0'
URI = f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER}.94tddj0.mongodb.net/?retryWrites=true&w=majority'
DATA_TO_DELETE_OLD_DATA_MONGODB = datetime.now() - timedelta(days=3)


# ======================================================


# ====================== DIRETÓRIOS LOCAIS e DATAS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_DIRECTORY = os.path.join(ROOT, "Data")
NOW = datetime.now().strftime("%d/%m %H:%M")
CURRENT_DAY = datetime.now().strftime("%d/%m")
# ===============================================================
