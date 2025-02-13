import constants_parc_ordinario
import authenticate 
import request
from datetime import datetime
#from authenticate import cnpjs_com_erro

# Processamento e caminho do arquivo gerado
processamento = 'PARCSN'
periodo_alvo = datetime.now().strftime('%Y%m') # Data atual no formato YYYYMM
data_atual = datetime.now().strftime('%Y%m%d')  # Data atual no formato YYYYMMDD
id_servico = "GERARDAS161"


if __name__ == "__main__":
    requisicoes_validas = 0
    requisicoes_falhas = 0
    cnpjs_erro = []
    # Autentica e gera o token de acesso
    authenticate.generate_bearer_token()

    for CLIENT_CODE in constants_parc_ordinario.CNPJS_LIST:
        # Define o caminho para o arquivo, agora utilizando o CLIENT_CODE da iteração
        caminho = f'/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/Arquivos_gerados/{id_servico}_{CLIENT_CODE}_{data_atual}'
        
        try:
            # Gera o arquivo de situação fiscal
            request.generate_data(processamento, caminho, id_servico, CLIENT_CODE)
            requisicoes_validas +=1 

        except:
            print(f"Erro na requisição do cliente: {CLIENT_CODE}")
            requisicoes_falhas += 1
            cnpjs_erro.append(CLIENT_CODE)
            

    print(f"{requisicoes_validas} requisições bem sucedidas.\n {requisicoes_falhas} requisições mal sucedidas. Clientes com status code diferentes de 200: {cnpjs_erro}")

