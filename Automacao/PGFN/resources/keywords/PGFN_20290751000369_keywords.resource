*** Settings ***
Library    /Users/rafaellacavalcante/Asteca/PROJETOS_REGEX/nomes.py
Library     OperatingSystem
Library     SeleniumLibrary
Library     DateTime
Resource    ../../../PGFN/tests/PGFN_20290751000369.robot
Resource    ../variables/PGFN_20290751000369_variables.robot
Resource    ../../../config/factory.robot


*** Keywords ***
Abrir pagina
    Open Browser    ${URL}    ${BROWSER}    
    Maximize Browser Window
Preencher os dados do cliente  
    Click Element    ${PERMITIR}
    Input Text    ${INPUT_CNPJ}    ${CNPJ}
    ${OBTER_PARC}=    Obter Parcelamento    ${CNPJ}
    Input Text    ${INPUT_PARCELAMENTO}    ${OBTER_PARC}

Clique no Checkbox
    Select Frame    ${IFRAME_XPATH}
    Click Element    ${CHECKBOX_CAPTCHA} 
    Unselect Frame 
    Sleep    1
Clique em "Consultar"
    Click Element    ${CONSULTAR}
    Sleep   1
Clicando em Download de documento
    Scroll Element Into View    ${MES_VIGENTE}
    Execute JavaScript    window.scrollBy(0, 500)   # Desce 500 pixels
    #Execute Javascript    window.scrollTo(0, document.body.scrollHeight)
    #Click Image    ${MES_VIGENTE}
    ${data_valida}=  Verificar Data Mes Ano
    Run Keyword If  ${data_valida}  Click Image  ${MES_VIGENTE}
    Page Should Contain   Parcela para emissão
    Sleep    2
    Click Button    ${Emitir}
    Sleep    2
    Click Element    ${Link_PDF}
    Sleep    2