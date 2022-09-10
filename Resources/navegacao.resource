*** Variable ***
# Resouce utilizado para guardar locators utilizados em todas as partes da aplicação

&{navegacao}    
...    header=xpath://div[@id="__APP"]
...    btn_carteira_spot=xpath://*[contains(text(),"Carteira Spot")]
...    cookies=xpath://*[@id="onetrust-accept-btn-handler"]
...    initial_modal=xpath://*[contains(text(),"Bem-vindo à Binance Spot")]
...    modal_secund=xpath://*[@id="coachmark"]
...    btn_modal_secund=xpath://*[@id="margin-guide-tradeGuide-5-ok"]
...    header_login=xpath://*[@id="header_login"]
...    scroll_lower=xpath://*[@data-testid="OpenOrder"]
...    btn_skip_modal=xpath://span[@id="margin-guide-tradeGuide-0-skip"]
...    btn_close_modal_initial=xpath://*[contains(text(), "Bem-vindo à Binance Spot")]/../../..//*[local-name() = 'svg']


&{buy}
...    input_buy_quantity=xpath://*[@id="FormRow-BUY-total"]
...    btn_buy=xpath://*[@id="orderformBuyBtn"]
...    market_order=xpath://span[@data-testid="MarketType"]
...    balance=xpath://*[@class="proInnerForm"][1]//div[contains(text(),"Disponível")]/..//span
...    price_crypto=xpath://*[@class="showPrice"]
...    popup_order_buy=xpath://*[contains(@class,"bn-notification-body-wrapper")] //*[contains(text(), "Ordem Market de Compra Preenchida")]
...    error_to_buy=xpath://*[@id="autoFormBUY"]//div[contains(@class,"bn-input-status-error")]
...    modal_warning=xpath://*[@id="orderform-checked-reminders"]
...    btn_modal_warning=xpath://*[@id="orderform-checked-reminders"]/../../../../../..//*[contains(text(),"Confirmar")]


&{sell}
...    btn_stop_limit=xpath://span[@data-testid="stopLimit"]
...    input_sell_stop=xpath://*[@id="FormRow-SELL-stopPrice"]
...    input_sell_limit=xpath://*[@id="FormRow-SELL-stopLimitPrice"]
...    input_sell_quantity=xpath://*[@id="FormRow-SELL-quantity"]
...    balance_crypto=xpath://*[@class="proInnerForm"][2]//div[contains(text(),"Disponível")]/..//span
...    btn_sell=xpath://*[@id="orderformSellBtn"]
...    btn_modal_stop_limit=xpath://*[@data-bn-type="button"][contains(text(),"Confirmar")]
...    popup_order_sell=xpath://*[contains(@class,"bn-notification-body-wrapper")] //*[contains(text(), "Ordem Market de Venda Preenchida")]
...    error_to_sell=xpath://*[@id="autoFormSELL"]//div[contains(@class,"bn-input-status-error")]
...    slider_100=xpath://*[@id="autoFormSELL"]//div[contains(@class,"bn-slider-container")]/div[9]

&{orders_stop_list}
...    list_orders_stop=xpath://*[@data-testid="tradeInfoTable"]/div/div/div[{index}]
...    order_stop=xpath://*[@data-testid="tradeInfoTable"] //*[contains(text(),"{order_stop}")]
...    cancel_order=xpath://*[@data-testid="tradeInfoTable"]//*[contains(text(),"{cancel_order_s}")]/..//*[@id="cancel-order"]//*[local-name() = 'svg'][1]

&{search}
...    search_crypto=xpath://*[@data-testid="searchInput"]
...    crypto=xpath://*[@class="item item-symbol"]/.//*[contains(text(),"{formated_crypto}")]
...    confirm_crypto=xpath://div[@data-bn-type="text"]/h1[contains(text(),"{scrypto}")]


&{order_list}
...    open_orders_list=xpath://*[@class="list-grid"]/div
...    open_orders=xpath://*[@class="list-grid"]/.//*[contains(text(),"{...}")]


&{telegram}
...    group=xpath://*[@class="chatlist"]/a[1]

...    msg_body=xpath://div[@data-message-id="{counter}"]//*[@class="text-content with-meta"]

