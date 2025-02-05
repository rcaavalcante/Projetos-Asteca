*** Settings ***
Resource    ../../PGFN/resources/keywords/PGFN_GILVAN_AUTO_CENTER_keywords.resource

*** Test Cases ***
Caso de teste - Acessando o site PGFN e Buscando Parcelamento
    [Tags]    gilvan    parc1
    Abrir pagina
    Preencher os dados do cliente
    Clique no Checkbox
    Clique em "Consultar"
    Clicando em Download de documento

Caso de teste - Acessando o site PGFN e Buscando Parcelamento 02
    [Tags]    gilvan    parc2
    Abrir pagina
    Preencher os dados do cliente Parc 02
    Clique no Checkbox
    Clique em "Consultar"
    Clicando em Download de documento

Caso de teste - Acessando o site PGFN e Buscando Parcelamento 03
    [Tags]    gilvan    parc3
    Abrir pagina
    Preencher os dados do cliente Parc 03
    Clique no Checkbox
    Clique em "Consultar"
    Clicando em Download de documento