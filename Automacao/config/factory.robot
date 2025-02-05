*** Settings *** 
Library    SeleniumLibrary

*** Variables ***

#ADICONE AQUI O ID DO MES VIGENTE PARA REALIZAR O DOWNLOAD
${MES_VIGENTE}    (//img[@src='/sisparInternet/resources/imagens/imprimir.png'])[2]

*** Keywords ***
Verificar Data Mes Ano
    ${resultado}=  verificar_data_mes_ano
    Return From Keyword  ${resultado}