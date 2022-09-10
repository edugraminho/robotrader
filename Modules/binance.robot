*** Settings ***
Resource    ${ROOT}/Resources/main.resource

*** Keywords ***

Entrar na binance
    ${status_cook}    Run Keyword And Return Status    Wait Until Element Is Visible    ${navegacao.cookies}    timeout=5
    IF    ${status_cook}
        Wait Until Keyword Succeeds    3x    1s    Click Element    ${navegacao.cookies}
    END
    Wait Until Element Is Visible    ${navegacao.initial_modal}    timeout=2

    # Modal inicial
    ${status_modal}    Run Keyword And Return Status    Click Element    ${navegacao.btn_close_modal_initial}
    IF    ${status_modal} == ${False}
        ${status_modal}    Run Keyword And Return Status    Wait Until Keyword Succeeds    3x    1s    Click Element    ${navegacao.btn_close_modal_initial}
    END

    Wait Until Keyword Succeeds    3x    1s    Double Click Element    ${navegacao.btn_skip_modal}

    Click Element    ${navegacao.header_login}

    Log    Aguardando a leitura do QRCODE   console=True
    ${start}    Run Keyword And Return Status    Wait Until Element Is Visible   ${buy.btn_buy}    timeout=10m

    ${start_modal_sec}    Run Keyword And Return Status    Wait Until Element Is Visible   ${navegacao.modal_secund}    timeout=3

    IF    ${start_modal_sec}
        ${start_modal_sec}    Run Keyword And Return Status    Wait Until Keyword Succeeds    3x    1s    Double Click Element    ${navegacao.btn_modal_secund}
    END
    
    [Return]    ${start}


Adicionar crypto na barra de pesquisa
    [Arguments]    ${crypto}
    # Binance
    Switch Browser    2

    Log    ========================== Crypto Atual: ${crypto} ==========================   console=True
    Log    ===========================================================================   console=True

    Scroll Element Into View   ${search.search_crypto}

    Click Element    ${search.search_crypto}
    Press Keys    ${search.search_crypto}    CTRL+a+BACKSPACE
    Input Text    ${search.search_crypto}    ${crypto}

    ${listed_crypto}    Format String    ${search.crypto}    formated_crypto=${crypto[:-4]}

    # Verifica se a crypto foi add na de pesquisa
    ${status_listed_crypto}    Run Keyword And Return Status    Wait Until Element Is Visible    ${listed_crypto}    timeout=5
    IF    ${status_listed_crypto}
        Click Element    ${listed_crypto}
    ELSE
        Click Element    ${search.search_crypto}
        Press Keys    ${search.search_crypto}    CTRL+a+BACKSPACE
        Input Text    ${search.search_crypto}    ${crypto}
    END

    ${conf_crypto}    Format String    ${search.confirm_crypto}    scrypto=${crypto[:-4]}

    # Verifica se a crypto foi add no header esquerdo
    ${status_conf_crypto}    Run Keyword And Return Status    Wait Until Element Is Visible    ${conf_crypto}    timeout=5
    IF    ${status_conf_crypto}
        Log    Crypto no Header: ${crypto[:-4]}    console=True
    ELSE
        Click Element    ${search.search_crypto}
        Press Keys    ${search.search_crypto}    CTRL+a+BACKSPACE
        Input Text    ${search.search_crypto}    ${crypto}
    END

    [Return]    ${status_conf_crypto}


Market order and buy, compra instantania
    [Arguments]    ${crypto}
    # Binance
    Switch Browser    2

    Log    Iniciando COMPRA da moeda: ${crypto}   console=True

    Scroll Element Into View   ${buy.input_buy_quantity}
    Click Element    ${buy.market_order}

    ${str_balance}    Get Element Attribute    ${buy.balance}    innerText
    ${balance}    convert_to_int    ${str_balance}
    Log    Saldo da Carteira - ${balance}    console=True

    # Agora valor fixo - config.py
    ${pay}    pay_a_percentage    ${balance}
    Log    Aporte da crypto - ${pay}    console=True

    Input Text    ${buy.input_buy_quantity}    ${pay}

    Scroll Element Into View    ${navegacao.scroll_lower}
    Press Keys    ${buy.input_buy_quantity}    TAB

    Click Element    ${buy.btn_buy}

    ${status_error_buy}    Run Keyword And Return Status    Page Should Contain Element    ${buy.error_to_buy}
    IF    ${status_error_buy}
        Log    Erro ao comprar moeda: ${crypto}   console=True
        ${status_buy}    Set Variable    ${False}
    ELSE
        ${status_buy}    Set Variable    ${True}

        ${status_popup_buy}    Run Keyword And Return Status    Wait Until Element Is Visible    ${buy.popup_order_buy}    timeout=2

        IF    ${status_popup_buy}
            Wait Until Element Is Not Visible    ${buy.popup_order_buy}    timeout=5
        END

        Log    Compra Realizada com sucesso!: ${crypto}    console=True

    END
    [Return]    ${status_buy}


Adiciona Stop Limit
    [Arguments]    ${crypto}
    # Binance
    Switch Browser    2

    Log    Iniciando STOP-LIMIT - ${crypto}   console=True

    Scroll Element Into View   ${sell.input_sell_quantity}
    Click Element    ${sell.btn_stop_limit}

    ${str_price_crypto}    Get Element Attribute    ${buy.price_crypto}    innerText
    ${price_crypto}    convert_balance_crypto_to_float    ${str_price_crypto}

    Log    Preco da Crypto - ${price_crypto}    console=True
    #Adiciona o STOP
    ${price_stop}    calculate_stop_limit    ${price_crypto}
    Input Text    ${sell.input_sell_stop}    ${price_stop}
    Log    STOP-LIMIT de - ${price_stop}    console=True

    ${str_balance_crypto}    Get Element Attribute    ${sell.balance_crypto}    innerText
    ${balance_crypto}    convert_balance_crypto_to_stop    ${str_balance_crypto}

    Log    Total Crypto - ${balance_crypto}    console=True

    Scroll Element Into View    ${navegacao.scroll_lower}

    # adiciona o total de moeda para vender
    #${balance_crypto_str}    Convert To String    ${balance_crypto}
    #Input Text    ${sell.input_sell_quantity}    ${balance_crypto_str}
    # CLica direto em 100% em vez de colocar o valor no input
    ${status_slider}    Run Keyword And Return Status    Click Element    ${sell.slider_100}
    Click Element    ${sell.btn_sell}

    ${status_sell}    Run Keyword And Return Status    Page Should Contain Element    ${sell.error_to_sell}
    IF    ${status_sell}
        Log    Erro ao adicionar stop na moeda ${crypto}   console=True
        ${status_stop_limit}    Set Variable    ${False}
    ELSE
        Wait Until Element Is Visible    ${sell.btn_modal_stop_limit}
        Click Element    ${sell.btn_modal_stop_limit}
        ${status_stop_limit}    Set Variable    ${True}
        Log    Stop realizado com sucesso! ${crypto}    console=True

    END

    [Return]    ${status_stop_limit}


Market order fechando signal, venda instantania
    [Arguments]    ${crypto_name}
    # Binance
    Switch Browser    2
           
    ${str_balance_crypto}    Get Element Attribute    ${sell.balance_crypto}    innerText
    ${balance_crypto}    convert_to_int    ${str_balance_crypto}
    Log    Fechando signal, venda instantania da moeda: ${crypto_name}   console=True
    Log    Total Crypto - ${balance_crypto}    console=True

    IF    ${balance_crypto} == ${0}
        Scroll Element Into View    ${navegacao.scroll_lower}
        Verifica lista de ordens Stop Limit    ${crypto_name}
        ${status_sell}    Set Variable    ${False}
    ELSE

        Verifica lista de ordens Stop Limit    ${crypto_name}

        Scroll Element Into View    ${buy.market_order}
        Click Element    ${buy.market_order}
    
        Scroll Element Into View    ${navegacao.scroll_lower}

        #Input Text    ${sell.input_sell_quantity}    ${balance_crypto}
        # CLica direto em 100% em vez de colocar o valor no input
        ${status_click}    Run Keyword And Return Status    Click Element    ${sell.slider_100}
    
        Click Element    ${sell.btn_sell}

        ${status_error_sell}    Run Keyword And Return Status    Page Should Contain Element    ${sell.error_to_sell}
        IF    ${status_error_sell}
            Log    Erro ao vender moeda    console=True
            ${status_sell}    Set Variable    ${False}

        ELSE
            ${status_popup_sell}    Run Keyword And Return Status    Wait Until Element Is Visible    ${sell.popup_order_sell}    timeout=2
            IF    ${status_popup_sell}
                Wait Until Element Is Not Visible    ${sell.popup_order_sell}    timeout=5
            END
            ${status_sell}    Set Variable    ${True}
            Log    Venda instantania efetuada com sucesso!    console=True
        END
    END

    [Return]    ${status_sell}



Verifica lista de ordens Stop Limit
    [Arguments]    ${crypto_name}
    # Verifica se existe ordem de stop limit aberto, se tiver cancela antes de vender
    # Binance
    Switch Browser    2
            
    FOR    ${index}    IN RANGE    1    50
        ${orders_stop_limit}    Format String    ${orders_stop_list.list_orders_stop}    index=${index}

        ${orders_status}    Run Keyword And Return Status    Scroll Element Into View    ${orders_stop_limit}
        IF    ${orders_status} == ${False}
            Exit For Loop
        END

        ${order_stop}    Format String    ${orders_stop_list.order_stop}    order_stop=${crypto_name[:-4]+"/USDT"}

        ${order_crypto}    Run Keyword And Return Status    Scroll Element Into View    ${order_stop}
        ${order_crypto}    Run Keyword And Return Status    Wait Until Element Is Visible    ${order_stop}    timeout=2
        IF    ${order_crypto} == ${True} and ${orders_status} == ${True}

            ${cancel_order}    Format String    ${orders_stop_list.cancel_order}    cancel_order_s=${crypto_name[:-4]+"/USDT"}

            ${status_cancel}    Run Keyword And Return Status    Click Element    ${cancel_order}
            IF    ${status_cancel}
                Log    Ordem Cancelada com Sucesso! ${crypto_name[:-4]}    console=True
            ELSE
                Log    Falhou ao Cancelar a Ordem ${crypto_name[:-4]}    console=True
            END
        END
    END



Market flux
    # Binance
    Switch Browser    2

    #pegar o ultimo index_signal escrito no csv
    ${last_index_signal}    last_line_index_signal

    FOR    ${counter}    IN RANGE    ${last_index_signal}    999999
        #===================================================================================
        #  Fluxo captura de Sinais Telegram
        #===================================================================================
            
        #Signals
        Switch Browser    1

        # vai buscar o body da msg pelo counter do for
        ${body_msg}    Format String    ${telegram.msg_body}    counter=${counter}
        ${hour_msg}    Format String    ${telegram.msg_date}    counter=${counter}

        ${Reload}    Run Keyword And Return Status    Page Should Contain Element    ${body_msg}
            
        Log    Aguardando novo sinal...   console=True

        WHILE    ${Reload} != ${TRUE}
            #Signals
            Switch Browser    1
            Reload Page
            Sleep    ${TIMEOUT_RELOAD_PAGE_SIGNALS}
            ${Reload}    Run Keyword And Return Status    Page Should Contain Element    ${body_msg}
        END

        ${last_index}    last_index

        Scroll Element Into View    ${body_msg}
        ${value}    Get Element Attribute    ${body_msg}    innerText
        ${hour_spot}    Get Element Attribute    ${hour_msg}    innerText
        Log    ${value}   console=True
        insert_csv    ${value}    ${counter}    ${hour_spot}    ${last_index}

        ${spot}    last_spot_dict

        Log    *********** Index: ${spot["index_signal"]} ***********    console=True
        Log    *********** Crypto: ${spot["crypto_name"]} ***********    console=True
        Log    *********** Signal Type: ${spot["signal_type"]} ***********    console=True
            

        #===================================================================================
        #  Fluxo de compra e venda Binance
        #===================================================================================
        # Binance
        Switch Browser    2

        Log    Adicionando crypto na barra de pesquisa - ${spot["crypto_name"]}   console=True
        Adicionar crypto na barra de pesquisa    ${spot["crypto_name"]}

        IF    "${spot["signal_type"]}" == "New signal" and '${spot["buy_or_sell"]}' == "new"

            ${status_buy}    Market order and buy, compra instantania    ${spot["crypto_name"]}
            ${status_stop_limit}    Adiciona Stop Limit    ${spot["crypto_name"]}
            
            #só altera o CSV se der certo a Compra e o Stop
            IF    ${status_stop_limit} == ${True} and ${status_buy} == ${True}
                insert_csv_buy_or_sell    ${spot["index"]}    buy
            END

        END

        IF    "${spot["signal_type"]}" == "Signal closed" and '${spot["buy_or_sell"]}' == "new"
            #Só Altera o csv se der certo a venda
            ${status_sell}    Market order fechando signal, venda instantania    ${spot["crypto_name"]}
            IF    ${status_sell}
                insert_csv_buy_or_sell    ${spot["index"]}    sell
            END
        END

        Log    ===========================================================================   console=True
        Log    ===========================================================================   console=True

    END