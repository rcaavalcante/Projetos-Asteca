*** Settings ***
Resource    ../../PGFN/resources/keywords/PGFN_20290751000369_keywords.resource
Library    ../../config/

*** Test Cases ***
Caso de teste - Acessando o site PGFN e Buscando Parcelamento
    [Tags]     cliente    principal
    Abrir pagina
    Preencher os dados do cliente
    Clique no Checkbox
    Clique em "Consultar"
    Clicando em Download de documento
    

    