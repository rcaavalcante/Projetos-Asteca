from Gerando_Tabela_ADS import gerando_arquivo
def cadastrar_empresas():
    # Inicializando as listas
    empresas_ads = []
    cod_empresas = []
    vigencia = []
    tipos_contrato = []

    # Pergunta quantas empresas o usuário deseja cadastrar
    qtde_empresa = int(input("Quantas empresas você deseja cadastrar? "))

    # Laço para cadastrar as empresas e seus códigos
    for i in range(qtde_empresa):
        empresa = input(f"Digite o nome da empresa {i+1}: ").capitalize()
        empresas_ads.append(empresa)  # Adiciona o nome da empresa à lista

        # Exibe o nome da empresa e pede o código correspondente
        codigo = int(input(f"Digite o código da empresa {empresa}: "))
        cod_empresas.append(codigo)  # Adiciona o código à lista

        # Pergunta o status do contrato (Ativo ou Inativo)
        while True:
            contrato = input(f"Qual o status do contrato da empresa {empresa} (Ativo ou Inativo)? ").capitalize()
            if contrato in ['Ativo', 'Inativo']:
                vigencia.append(contrato)  # Adiciona o status do contrato à lista
                break  # Sai do loop caso a entrada seja válida
            else:
                print("Erro: O status do contrato deve ser 'Ativo' ou 'Inativo'. Tente novamente.")

        # Pergunta o tipo do contrato (Fixo ou Temporário)
        while True:
            tipo_contrato = input(f"Qual o tipo de contrato da empresa {empresa} (Fixo ou Temporário)? ").capitalize()
            if tipo_contrato in ['Fixo', 'Temporário', 'Temporario']:
                tipos_contrato.append(tipo_contrato)  # Adiciona o tipo de contrato à lista
                break  # Sai do loop caso a entrada seja válida
            else:
                print("Erro: O tipo de contrato deve ser 'Fixo' ou 'Temporário'. Tente novamente.")

    # Exibe as listas de empresas e seus dados
    print(f"A lista de empresas cadastradas é: {empresas_ads}\n"
          f"Os códigos das empresas são: {cod_empresas}\n"
          f"Os status dos contratos são: {vigencia}\n"
          f"Os tipos de contrato são: {tipos_contrato}")

    # Chama a função para gerar o arquivo Excel
    gerando_arquivo(empresas_ads, cod_empresas, vigencia, tipos_contrato, "empresas_cadastradas.xlsx",
                    "Nome da Empresa", "Código da Empresa", "Status do Contrato", "Tipo de Contrato")


# Chama a função para executar
cadastrar_empresas()





