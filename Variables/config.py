from pathlib import Path, PurePath
import os
from datetime import datetime


TIMEOUT_RELOAD_PAGE_SIGNALS = 10

# ==================== WALLET ==========================
# valor de aporte por moeda
PURCHASE_VALUE = 15
STOP_LOSS_PERCENTAGE = 8
PURCHASE_PERCENTAGE = 3
# ======================================================

# ==================== API TELEGRAM ====================
API_ID = 11074177
API_HASH = '15a39f85549bd32cd83935b3dd04d26c'
# ======================================================

# ==================== CHROME ==========================
URL = "https://www.binance.com/en/futures/BTCUSDT"
URL_SIGNALS = "https://web.telegram.org/"
BROWSER_DIRECTORY = "C:\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
CHROMEDRIVER_DIRECTORY = "C:\\chromedriver\\chromedriver.exe"
# ======================================================

# =================== Timeout Robot ====================
DEFAULT_SELENIUM_TIMEOUT = '40 seconds'
DEFAULT_DOWNLOAD_TIMEOUT = '60 seconds'
# ======================================================

# ====================== DIRETÓRIOS LOCAIS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
NOW = datetime.now().strftime("%d%m - %H:%M")
DATA_DIRECTORY = os.path.join(ROOT, "Data")
# ===============================================================
