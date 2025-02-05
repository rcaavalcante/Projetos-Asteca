import os
import base64
import json
import requests
import xml.etree.ElementTree as eT
from time import sleep
from constants import URL_REQUEST, URL_TRANSMIT, URL_SUPPORT, API_SECRETS, ACCOUNTANT_CODE, CNPJS_LIST, read_keys


def generate_data(modulo, caminho, periodo):
    read_keys()
    header = {
        "Authorization": f"Bearer {API_SECRETS.get('accessToken')}",
        "content-type": "application/json",
        "jwt_token": API_SECRETS.get('jwtToken')
    }
    data = {
        "contratante": {
            "numero": ACCOUNTANT_CODE,
            "tipo": 2
        },
        "autorPedidoDados": {
            "numero": ACCOUNTANT_CODE,
            "tipo": 2
        },
        "contribuinte": {
            "numero": CLIENT_CODE,
            "tipo": 2
        },
    }
    url = ''

    if modulo == 'sit_fiscal':
        data["pedidoDados"] = {
            "idSistema": "SITFIS",
            "idServico": "SOLICITARPROTOCOLO91",
            "versaoSistema": "2.0",
            "dados": ""
        }

        support = requests.post(URL_SUPPORT, data=json.dumps(data), headers=header)

        if support.status_code == 304:
            value = support.headers.get('etag').split(":", 1)[1].strip('"')
            wait = 0
        else:
            content = json.loads(support.json().get('dados'))
            value = content.get('protocoloRelatorio')
            wait = int(content.get('tempoEspera')) / 100

        data["pedidoDados"]["idServico"] = "RELATORIOSITFIS92"
        data["pedidoDados"]["versaoSistema"] = "2.0"
        data["pedidoDados"]["dados"] = '{{ "protocoloRelatorio":  "{}" }}'.format(value)

        url = URL_TRANSMIT

        sleep(wait)

    res = requests.post(url, data=json.dumps(data), headers=header)
    print(f'Status code da requisição {modulo}: {res.status_code}')
    print("Solicitação", res)
    print(res.status_code)