import json

# Caminho para o arquivo keys.json
KEYS_FILE = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Integra_Contador/Files/keys.json'


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
           "00075112000101",
            "00597582000135",
            "01479626000195",
            "01496359000750",
            "01682442000128",
            "01739861000159",
            "02321770000161",
            "02374034000171",
            "02494299000103",
            "02541065000170",
            "02715000000101",
            "03356754000177",
            "04918941000160",
            "04956309000100",
            "05195537000178",
            "05605725000127",
            "05764194000115",
            "06219783000185",
            "06227480000104",
            "06299272000110",
            "06341035000170",
            "07069527000111",
            "07916671000146",
            "08139911000106",
            "08865892000103",
            "08870403000101",
            "09400550000172",
            "09404882000125",
            "09615457000185",
            "10139647000152",
            "10556232000184",
            "10759594000172",
            "10829906000177",
            "11145516000140",
            "12525292000165",
            "15343435000106",
            "15735291000133",
            "17219586000182",
            "17844578000127",
            "17910909000180",
            "18309699000131",
            "20276958000117",
            "20290751000369",
            "20373154000136",
            "20769676000151",
            "21340293000398",
            "21778116000126",
            "22336007000111",
            "24185633000180",
            "24865643000166",
            "25024092000170",
            "25141771000120",
            "26920835000153",
            "27732407000160",
            "30449282000170",
            "30821927000153",
            "31385027000173",
            "31839487000124",
            "32429411000193",
            "32944766000110",
            "33262015000187",
            "34778620000178",
            "37088659000151",
            "37167362000181",
            "37794160000160",
            "37839594000139",
            "39682413000139",
            "39818429000126",
            "42125797000101",
            "43020321000160",
            "43214851000140",
            "43940515000184",
            "45037229000139",
            "45619362000101",
            "46262674000165",
            "46503012000130",
            "46953166000123",
            "47079965000185",
            "47646012000151",
            "47676876000116",
            "47807337000179",
            "47986571000100",
            "49231794000193",
            "50394171000110",
            "51747386000130",
            "51995820000100",
            "52074987000192",
            "54264657000195",
            "54399127000154",
            "55436655000107",
            "55480173000146",
            "56193953000178",
            "56480235000182",
            "57615441000115",
            "57723469000176",
            "57864754000107",
            "97545949000109"
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
