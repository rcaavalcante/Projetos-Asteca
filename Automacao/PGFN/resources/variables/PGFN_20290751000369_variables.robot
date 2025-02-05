*** Settings ***
Library    /Users/rafaellacavalcante/Asteca/PROJETOS_REGEX/nomes.py

*** Variables ***

#Primeira etapa
${URL}     https://sisparnet.pgfn.fazenda.gov.br/sisparInternet/internet/darf/consultaParcelamentoDarfInternet.xhtml
${BROWSER}     Chrome
${TIME_OUT}    10
${PERMITIR}   xpath=//*[contains(text(), "Permitir")]

#ELEMENTOS HTML LOGIN
${INPUT_CNPJ}    id=formConsultaParcelamentoDarf:imNrCpfCnpjParcelamento
${INPUT_PARCELAMENTO}    id=formConsultaParcelamentoDarf:imNrContaParcelamento
${IFRAME_XPATH}    xpath://iframe[contains(@src, 'hcaptcha')]
${CHECKBOX_CAPTCHA}    //div[contains(@id, 'checkbox')]
${CONSULTAR}    class=ui-button-text

#Segunda etapa
# Pega o mês atual
${XPATH_TABELA}    /html/body/div[1]/div[2]/div[2]/div/form/fieldset[2]/div/div/table/tbody/tr/td[4]/div
${Elemento_parc}    id=formResumoParcelamentoDarf\:btnVoltar
${Emitir}    id=formResumoParcelamentoDarf\:btnEmitir
${Link_PDF}    id=formResumoParcelamentoDarf\:emitirDarf

#CNPJS UTILIZADOS PARA REALIZAR LOGIN NA PGFN - ABC
${CNPJ}    00075112000101
${Parcelamento}    ${obter_parcelamento(${CNPJ})}

