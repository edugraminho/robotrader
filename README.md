# README #

Iniciar Projeto
pipenv run python trader.py 


App api_id:
11074177

App api_hash:
15a39f85549bd32cd83935b3dd04d26c


Name:
getMessages

Test configuration:
149.154.167.40:443


Public keys:
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAyMEdY1aR+sCR3ZSJrtztKTKqigvO/vBfqACJLZtS7QMgCGXJ6XIR
yy7mx66W0/sOFa7/1mAZtEoIokDP3ShoqF4fVNb6XeqgQfaUHd8wJpDWHcR2OFwv
plUUI1PLTktZ9uW2WE23b+ixNwJjJGwBDJPQEQFBE+vfmH0JP503wr5INS1poWg/
j25sIWeYPHYeOrFp/eXaqhISP6G+q2IeTaWTXpwZj4LzXq5YOpk4bYEQ6mvRq7D1
aHWfYmlEGepfaYR8Q0YqvvhYtMte3ITnuSJs171+GDqpdKcSwHnd6FudwGO4pcCO
j4WcDuXc2CTHgH8gFTNhp/Y8/SpDOhvn9QIDAQAB
-----END RSA PUBLIC KEY-----


Production configuration:
149.154.167.50:443

Public keys:
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEA6LszBcC1LGzyr992NzE0ieY+BSaOW622Aa9Bd4ZHLl+TuFQ4lo4g
5nKaMBwK/BIb9xUfg0Q29/2mgIR6Zr9krM7HjuIcCzFvDtr+L0GQjae9H0pRB2OO
62cECs5HKhT5DZ98K33vmWiLowc621dQuwKWSQKjWf50XYFw42h21P2KXUGyp2y/
+aEyZ+uVgLLQbRA1dEjSDZ2iGRy12Mk5gpYc397aYp438fsJoHIgJ2lgMv5h7WY9
t6N/byY9Nw9p21Og3AoXSL2q/2IJ1WRUhebgAdGVMlV1fkuOQoEzR7EdpqtQD9Cs
5+bfo3Nhmcyvk5ftB0WkJ9z6bNZ7yxrP8wIDAQAB
-----END RSA PUBLIC KEY-----



# Tratamento de erro Binance
    except ValueError as e:
        raise BinanceAPIException(e.response, e.status_code, e.text)
        print(e.status_code)
        print(e.message)
        print(e.response)
        print(e.request)
        print(e.code)




    # pegar o retorno e armnazenar o orderId
    futures_order = {
        "orderId":74842174826,
        "symbol":"BTCUSDT",
        "status":"NEW",
        "clientOrderId":"pjUADBlrl43eKRQkt1WhBy",
        "price":"0",
        "avgPrice":"0.00000",
        "origQty":"0.010",
        "executedQty":"0",
        "cumQty":"0",
        "cumQuote":"0",
        "timeInForce":"GTC",
        "type":"MARKET",
        "reduceOnly":False,
        "closePosition":False,
        "side":"BUY",
        "positionSide":"LONG",
        "stopPrice":"0",
        "workingType":"CONTRACT_PRICE",
        "priceProtect":False,
        "origType":"MARKET",
        "updateTime":1662843258272
        }