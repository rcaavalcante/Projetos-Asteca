import Projetos_API.API_Parcelamentos.PARCSN_ORDINARIO.constants_parc_ordinario as constants_parc_ordinario
import authenticate
import request
from datetime import datetime


# Processamento e caminho do arquivo gerado
processamento = 'sit_fiscal'
data_atual = datetime.now().strftime('%Y%m%d')  # Data atual no formato YYYYMMDD


if __name__ == "__main__":
    requisicoes_validas = 0
    requisicoes_falhas = 0
    cnpjs_erro = []
    # Autentica e gera o token de acesso
    authenticate.generate_bearer_token()

    for CLIENT_CODE in constants_parc_ordinario.CNPJS_LIST:
        # Define o caminho para o arquivo, agora utilizando o CLIENT_CODE da iteração
        caminho = f'/Users/rafaellacavalcante/Asteca/Projetos_API/API_Integra_Contador/Files/Arquivos_gerados/Situação Fiscal_{CLIENT_CODE}_{data_atual}.pdf'
        
        try:
            # Gera o arquivo de situação fiscal
            request.generate_data(processamento, caminho, '241201', CLIENT_CODE)
            requisicoes_validas +=1 

        except:
            print(f"Erro na requisição do cliente: {CLIENT_CODE}")
            requisicoes_falhas += 1
            cnpjs_erro.append(CLIENT_CODE)
            

    print(f"{requisicoes_validas} requisições bem sucedidas.\n {requisicoes_falhas} requisições mal sucedidas. Clientes com status code diferentes de 200: {cnpjs_erro}")