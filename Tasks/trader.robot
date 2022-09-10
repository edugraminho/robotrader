*** Settings ***
Documentation    Arquivo de recursos
Resource    ${ROOT}/Resources/main.resource


*** Tasks ***
Abrir Browser
    [Documentation]    Task que abre o browser e retorna seu status

    ${status_sig}    Run Keyword And Return Status    Abrir Navegador    ${URL_SIGNALS}
    Entrar Telegram

    Capturar lista

    # ${status}    Run Keyword And Return Status    Abrir Navegador    ${URL}
    # ${bin_status}    Aguardar Pagina Carregar    ${navegacao.header}
    
    # ${start}    Entrar na binance

    # IF    ${start}
    #     Set Next Task    Fluxo de Compra e Venda
    # END


Fluxo de Compra e Venda
    Market flux



Finaliza Processo
    [Documentation]    Task de finalização do robô

    Log    Finalizando Processo!    level=INFO
    Fechar Navegador

# TODO
# refatorar o fluxo de venda
# remover moeda quando ser fechada por stop
# validacao para aquele modal de 24hrs        - ja mapeado     buy.modal_warning     buy.btn_modal_warning
# falha ao cancelar ordem
# funcao para adicionar manualmente SPOT