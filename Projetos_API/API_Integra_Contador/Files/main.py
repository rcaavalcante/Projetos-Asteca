import constants
import authenticate
import request
from datetime import datetime
#from authenticate import cnpjs_com_erro

# Processamento e caminho do arquivo gerado
processamento = 'sit_fiscal'
data_atual = datetime.now().strftime('%Y%m%d')  # Data atual no formato YYYYMMDD


if __name__ == "__main__":
    # Autentica e gera o token de acesso
    authenticate.generate_bearer_token()

    for CLIENT_CODE in constants.CNPJS_LIST:
        # Define o caminho para o arquivo, agora utilizando o CLIENT_CODE da iteração
        caminho = f'/Users/rafaellacavalcante/Asteca/Projetos_API/API_Integra_Contador/Files/Arquivos_gerados/Situação Fiscal_{CLIENT_CODE}_{data_atual}.pdf'
        
        # Gera o arquivo de situação fiscal
        request.generate_data(processamento, caminho, '241201', CLIENT_CODE)

