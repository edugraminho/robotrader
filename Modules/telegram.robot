*** Settings ***
Resource    ${ROOT}/Resources/main.resource

*** Keywords ***
Entrar Telegram
    Log    Aguardando a leitura do QRCODE   console=True

    ${status}    Run Keyword And Return Status    Wait Until Element Is Visible    ${telegram.group}   timeout=1m
    IF    ${status}
        Click Element    ${telegram.group}
    END

Capturar lista
    #TODO pegar o ultimo index escrito no csv
    ${last_index_signal}    last_line_index_signal

    FOR    ${counter}    IN RANGE    59315    999999
    # FOR    ${counter}    IN RANGE    5070    999999

        ${body_msg}    Format String    ${telegram.msg_body}    counter=${counter}

        ${Reload}    Run Keyword And Return Status    Page Should Contain Element    ${body_msg}
        WHILE    ${Reload} != ${TRUE}
            Reload Page
            Sleep    10
            Log    Aguardando novo sinal...   console=True
            ${Reload}    Run Keyword And Return Status    Page Should Contain Element    ${body_msg}
        END
        ${last_index}    last_index

        Scroll Element Into View    ${body_msg}
        ${value}    Get Element Attribute    ${body_msg}    innerText
        Log    ${value}   console=True
        insert_csv    ${value}    ${counter}    ${hour_spot}    ${last_index}
    END

