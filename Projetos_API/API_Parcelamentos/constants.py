import json

# Caminho para o arquivo keys.json
KEYS_FILE = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/keys.json'


# Carrega as credenciais da API a partir do arquivo keys.json
with open(KEYS_FILE) as keys:
    secrets = keys.read()

# Endpoints da API que serão utilizados para autenticação e chamadas de serviços
URL_AUTH = 'https://autenticacao.sapi.serpro.gov.br/authenticate'
URL_REQUEST = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Consultar'
URL_TRANSMIT = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Emitir'
URL_SUPPORT = 'https://gateway.apiserpro.serpro.gov.br/integra-contador/v1/Apoiar'

# Caminho para o arquivo de certificado digital .pfx e sua senha
CERT_FILE = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Integra_Contador/Files/astecacontabilidade.pfx'
CERT_PASS = 'Asteca'

# Carregamento das Credenciais no formato de dicionário
API_SECRETS = json.loads(secrets)

# Códigos de Identificação
ACCOUNTANT_CODE = '33262015000187'
WARRANT_CODE = ''
#CLIENT_CODE = '33262015000187'
CNPJS_LIST = [ 
            '15343435000106',
            '00075112000101'
            ]


# Função para atualizar o arquivo keys.json com novos atributos
def append_attributes(key, value):
    with open(KEYS_FILE) as f:
        data = json.load(f)
    data.update({key: value})
    with open(KEYS_FILE, 'w') as f:
        json.dump(data, f)

# Função para recarregar as chaves do arquivo keys.json
def read_keys():
    global API_SECRETS

    with open(KEYS_FILE) as chaves:
        sec = chaves.read()
    API_SECRETS = json.loads(sec)
    return API_SECRETS
