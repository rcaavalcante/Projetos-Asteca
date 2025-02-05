import base64
import json
from requests_pkcs12 import post
from API.Files.constants import URL_AUTH

# converte as credenciais para base64
def converter_base64(credenciais):
    return base64.b64encode(credenciais.encode("utf8")).decode("utf8")


def serpro_componentes_autenticacaoLoja():
    url = URL_AUTH
    
    # Caminho para o arquivo PFX (certificado)
    certificado = 'API/Files/astecacontabilidade.pfx'
    senha = 'sEnha_do_certificado'
    
    # credenciais loja Serpro para autenticação
    consumer_key = "YIqPy6KHyZaFcKFOuk0cZSmc5TMa"
    consumer_secret = "vz6mqYazkbZkn0KJdgbg5M5hfv0a"
    
    # Cabeçalhos para autenticação
    headers = {
        "Authorization": "Basic " + converter_base64(consumer_key + ":" + consumer_secret),
        "role-type": "TERCEIROS",
        "content-type": "application/x-www-form-urlencoded"
    }

    # Corpo da requisição
    body = {'grant_type': 'client_credentials'}

    # Realizando a requisição com o certificado digital
    response = post(
        url,
        data=body,
        headers=headers,
        verify=True,
        pkcs12_filename=certificado,
        pkcs12_password=senha
    )

    # Retornar a resposta
    return response


# Chamada da função de autenticação
response = serpro_componentes_autenticacaoLoja()

# Exibindo os resultados
print(response.status_code)
print(json.dumps(response.json(), indent=4, separators=(',', ': '), sort_keys=True))