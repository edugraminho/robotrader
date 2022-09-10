*** Settings ***
Library    SeleniumLibrary    run_on_failure=NOTHING
Library    DebugLibrary
Library    String
Library    Collections
Library    OperatingSystem
Library    DateTime
Library    RPA.Tasks

#========= Custom Libraries ==========
Library    ${ROOT}/Libraries/chromedriver_utils.py
Library    ${ROOT}/Libraries/utils.py

#========= Keywords ==========
Resource    ${ROOT}/Modules/navegacao.robot
Resource    ${ROOT}/Modules/telegram.robot
Resource    ${ROOT}/Modules/binance.robot

#========= Locators ==========
Resource    ${ROOT}/Resources/navegacao.resource
