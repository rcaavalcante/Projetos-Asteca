*** Settings ***
Library     OperatingSystem
Library     SeleniumLibrary
Library     DateTime
Resource    ../../../PGFN/tests/PGFN_GILVAN_AUTO_CENTER.robot
Resource    ../variables/PGFN_GILVAN_AUTO_CENTER_variables.robot
Resource    ../../../config/factory.robot

*** Keywords ***
Abrir pagina
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
Preencher os dados do cliente  
    Click Element    ${PERMITIR}
    Input Text    ${INPUT_CNPJ}    ${CNPJ}
    Input Text    ${INPUT_PARCELAMENTO}    ${Parcelamento_01}
Clique no Checkbox
    Select Frame    ${IFRAME_XPATH}
    Click Element    ${CHECKBOX_CAPTCHA} 
    Unselect Frame 
    Sleep    1
Clique em "Consultar"
    Click Element    ${CONSULTAR}
    Sleep   1
Clicando em Download de documento
    Execute JavaScript    window.scrollBy(0, 500)   # Desce 500 pixels
    Click Element    ${MES_VIGENTE}
    Page Should Contain   Parcela para emissão
    Sleep    2
    Click Button    ${Emitir}
    Sleep    2
    Click Element    ${Link_PDF}
    Sleep    2
Preencher os dados do cliente Parc 02
    Input Text    ${INPUT_PARCELAMENTO}    ${Parcelamento_02}

Preencher os dados do cliente Parc 03
    Input Text    ${INPUT_PARCELAMENTO}    ${Parcelamento_03}

