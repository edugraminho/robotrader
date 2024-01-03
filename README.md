
# Tratamento de erro Binance
    except ValueError as e:
        raise BinanceAPIException(e.response, e.status_code, e.text)
        print(e.status_code)
        print(e.message)
        print(e.response)
        print(e.request)
        print(e.code)

    #APIError(code=-2022): ReduceOnly Order is rejected
    #APIError(code=-4005): Quantity greater than max quantity.
    #{"code":-1102,"msg":"Mandatory parameter \'positionSide\' was not sent, was empty/null, or malformed."}
    #{"code":-4005,"msg":"Quantity greater than max quantity."





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




GET ALL POSITIONS


    {
        "symbol":"AVAXUSDT",
        "positionAmt":"16",
        "entryPrice":"17.03",
        "markPrice":"17.31106440",
        "unRealizedProfit":"4.49703040",
        "liquidationPrice":"0",
        "leverage":"20",
        "maxNotionalValue":"250000",
        "marginType":"cross",
        "isolatedMargin":"0.00000000",
        "isAutoAddMargin":"false",
        "positionSide":"LONG",
        "notional":"276.97703040",
        "isolatedWallet":"0",
        "updateTime":1664468887542
    }

    #SHORT
    {
        "symbol":"BTCUSDT",
        "positionAmt":"-0.005",
        "entryPrice":"19570.2",
        "markPrice":"19567.00422088",
        "unRealizedProfit":"0.01597889",
        "liquidationPrice":"154359.23249602",
        "leverage":"20",
        "maxNotionalValue":"10000000",
        "marginType":"cross",
        "isolatedMargin":"0.00000000",
        "isAutoAddMargin":"false",
        "positionSide":"SHORT",
        "notional":"-97.83502110",
        "isolatedWallet":"0",
        "updateTime":1664495026797
    }



    testando git-pull