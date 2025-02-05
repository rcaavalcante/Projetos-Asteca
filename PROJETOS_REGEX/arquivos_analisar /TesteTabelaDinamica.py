import pandas as pd

# Criar um DataFrame de exemplo
dados = {
    'Categoria': ['A', 'A', 'B', 'B'],
    'Produto': ['Produto 1', 'Produto 2', 'Produto 3', 'Produto 4'],
    'Vendas': [100, 150, 200, 250]
}

df = pd.DataFrame(dados)

# Adicionar uma linha mestre
linha_mestre = pd.DataFrame({'Categoria': ['Teste'], 'Produto': [''], 'Vendas': ['']})

# Concatenar a linha mestre com o DataFrame original
df_final = pd.concat([linha_mestre, df], ignore_index=True)

# Criar um ExcelWriter para inserir a linha mestre acima do cabeçalho
with pd.ExcelWriter('tabela_com_linha_mestre4.xlsx', engine='openpyxl') as writer:
    # Escrever a linha mestre como a primeira linha
    df_mestre = pd.DataFrame([['Linha Mestre', '', '']])  # Ajuste conforme necessário
    df_mestre.to_excel(writer, index=False, header=False, startrow=0)

    # Escrever o DataFrame final abaixo da linha mestre
    df_final.to_excel(writer, index=False, header=True, startrow=1)

# Exibir mensagem de confirmação
print("Arquivo Excel criado com a linha mestre acima dos títulos.")


