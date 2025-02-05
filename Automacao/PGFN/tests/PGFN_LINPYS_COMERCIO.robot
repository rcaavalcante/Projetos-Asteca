*** Settings ***
Resource    ../../PGFN/resources/keywords/PGFN_PARC_keywords.resource

*** Test Cases ***
Caso de teste - Acessando o site PGFN e Buscando Parcelamento
    [Tags]     linpys    parc1
    Abrir pagina
    Preencher os dados do cliente
    Clique no Checkbox
    Clique em "Consultar"
    Clicando em Download de documento