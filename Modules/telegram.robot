*** Settings ***
Resource    ${ROOT}/Resources/main.resource

*** Keywords ***
Entrar Grupo Telegram

    ${Reload}    Run Keyword And Return Status    Page Should Contain Element    ${telegram.group}
    WHILE    ${Reload} != ${TRUE}
        Sleep    5
        Log    Aguardando Logar    console=True
        ${Reload}    Run Keyword And Return Status    Page Should Contain Element    ${telegram.group}
    END

    Wait Until Keyword Succeeds    3x    1s    Click Element    ${telegram.group}


Capturar lista
    #TODO pegar o ultimo index escrito no csv
    ${last_index_signal}    last_line_index_signal

    FOR    ${counter}    IN RANGE    ${last_index_signal}    9999999
    # FOR    ${counter}    IN RANGE    5070    999999

        ${body_msg}    Format String    ${telegram.msg_body}    counter=${counter}
        # Debug
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
        insert_csv    ${value}    ${counter}    ${last_index}
    END

