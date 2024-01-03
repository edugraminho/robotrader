from pathlib import Path, PurePath
import os
from datetime import datetime, timedelta


# ==================== API BINANCE ====================
QNT_CRYPTOS_TO_PURCHASE = 100 #o maximo de cryptos a serem negociadas, total / pelo saldo
PERCENTAGE_STOP = 2
LEVERAGE = 20

LIST_TARGETS_TAKE_PROFITS = [4, 7]

# API_KEY EDU
API_KEY = "bxzxQ90y1LZPbGKFqRwA4FgtE9EZw1URhqwQgyFCLSW4jxJcvRLPhtrPzJuzojpR"
API_SECRET = "BgNL0J7xY3t1FD3xdvnGjiuqKE76XaMylWqKgELlKBsnmWNb8Rp8w16PHiAZEWTP"
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





# # README #

# Iniciar Projeto
# pipenv run python trader.py 


# App api_id:
# 11074177

# App api_hash:
# 15a39f85549bd32cd83935b3dd04d26c


# Name:
# getMessages

# Test configuration:
# 149.154.167.40:443


# Public keys:
# -----BEGIN RSA PUBLIC KEY-----
# MIIBCgKCAQEAyMEdY1aR+sCR3ZSJrtztKTKqigvO/vBfqACJLZtS7QMgCGXJ6XIR
# yy7mx66W0/sOFa7/1mAZtEoIokDP3ShoqF4fVNb6XeqgQfaUHd8wJpDWHcR2OFwv
# plUUI1PLTktZ9uW2WE23b+ixNwJjJGwBDJPQEQFBE+vfmH0JP503wr5INS1poWg/
# j25sIWeYPHYeOrFp/eXaqhISP6G+q2IeTaWTXpwZj4LzXq5YOpk4bYEQ6mvRq7D1
# aHWfYmlEGepfaYR8Q0YqvvhYtMte3ITnuSJs171+GDqpdKcSwHnd6FudwGO4pcCO
# j4WcDuXc2CTHgH8gFTNhp/Y8/SpDOhvn9QIDAQAB
# -----END RSA PUBLIC KEY-----


# Production configuration:
# 149.154.167.50:443

# Public keys:
# -----BEGIN RSA PUBLIC KEY-----
# MIIBCgKCAQEA6LszBcC1LGzyr992NzE0ieY+BSaOW622Aa9Bd4ZHLl+TuFQ4lo4g
# 5nKaMBwK/BIb9xUfg0Q29/2mgIR6Zr9krM7HjuIcCzFvDtr+L0GQjae9H0pRB2OO
# 62cECs5HKhT5DZ98K33vmWiLowc621dQuwKWSQKjWf50XYFw42h21P2KXUGyp2y/
# +aEyZ+uVgLLQbRA1dEjSDZ2iGRy12Mk5gpYc397aYp438fsJoHIgJ2lgMv5h7WY9
# t6N/byY9Nw9p21Og3AoXSL2q/2IJ1WRUhebgAdGVMlV1fkuOQoEzR7EdpqtQD9Cs
# 5+bfo3Nhmcyvk5ftB0WkJ9z6bNZ7yxrP8wIDAQAB
# -----END RSA PUBLIC KEY-----