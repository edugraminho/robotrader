from pathlib import Path, PurePath
import os
from datetime import datetime


# ==================== WALLET ==========================
# valor de aporte por moeda
PURCHASE_VALUE = 15
STOP_LOSS_PERCENTAGE = 8
PURCHASE_PERCENTAGE = 3
# ======================================================

# ==================== API BINANCE ====================
PERCENTAGE_BUY = 5
QNT_CRYPTOS_TO_PURCHASE = 45
PERCENTAGE_STOP = 3

API_KEY = "L8vTV38sqckhCZCT403TlRqxZHSGuASm95QckB9y5Hmg6g1OUddff79Y1k9DGGLb"
API_SECRET = "X4TE8ehw2891qrLgT4iQSoFn6kwnQXy1V6ispA34cdWf0kq9PXP9Xa1d1EW880Nt"
# ======================================================


# ==================== API TELEGRAM ====================
API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'
# ======================================================

# ====================== DIRETÓRIOS LOCAIS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
NOW = datetime.now().strftime("%d/%m %H:%M")
DATA_DIRECTORY = os.path.join(ROOT, "Data")
# ===============================================================
