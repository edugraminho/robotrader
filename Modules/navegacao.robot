*** Settings ***
Documentation    Biblioteca responsável por toda navegação do menu lateral
Resource    ${ROOT}/Resources/main.resource

*** Keywords ***
Fechar Navegador
    Close All Browsers

Abrir Navegador
    [Documentation]    Abre o navegador maximizado.

    [Arguments]    ${URL}
    ${prefs}    Create Dictionary    plugins.always_open_pdf_externally=${True}
    ${options}    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${options}    add_experimental_option    prefs    ${prefs}
    Call Method    ${options}    add_argument    start-maximized
    Call Method    ${options}    add_argument    disable-web-security
    Call Method    ${options}    add_argument    disable-notifications
    Call Method    ${options}    add_argument    disable-logging
    # Call Method    ${options}    add_argument    headless
    ${options.binary_location}    Browser Path
    ${chromedriver_path}    Chromedriver Path
    ${BrowserOpened}    Run Keyword And Return Status    Open Browser    ${URL}    Chrome    options=${options}    executable_path=${chromedriver_path}
    Set Selenium Timeout    ${DEFAULT_SELENIUM_TIMEOUT}
    # Set Window Size    ${1366}    ${720}

    [return]    ${BrowserOpened}


Aguardar Pagina Carregar
    [Arguments]    ${header}
    ${status}    Run Keyword And Return Status    Wait Until Element Is Visible    ${header}    timeout=5s

    [Return]    ${status}

