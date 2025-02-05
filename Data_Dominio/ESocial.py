import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o arquivo Excel
arquivo = '/Users/rafaellacavalcante/PycharmProjects/pythonProject/Asteca/Data_Dominio/Empresas_ESocial1.xls'

# Ler o arquivo Excel (pode ser .xls ou .xlsx)
df = pd.read_excel(arquivo)

# Dropar as colunas indesejadas
df = df.drop(columns=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 8', 'Unnamed: 10', 'Unnamed: 12', 'Unnamed: 14'])
df.drop(index=[0, 1, 2, 3, 4, 5, 6], inplace=True)


# Renomear as colunas
novos_nomes = ['Empresa', 'Ambiente', 'Competência', 'Status', 'Fase 1', 'Fase 2', 'Data de Emissão']
df.columns = novos_nomes

# Exibir os novos nomes das colunas
#print(df.columns.tolist())

# Exibir as primeiras linhas do DataFrame processado
print(df.head())


# Gráfico 1: Contagem de empresas por 'Status'
status_counts = df['Status'].value_counts()

# Criar o gráfico de barras
plt.figure(figsize=(10, 6))
ax = status_counts.plot(kind='bar')

# Adicionar as quantidades dentro das barras
for i, value in enumerate(status_counts):
    ax.text(i, value + 0.2, str(value), ha='center', va='bottom', fontsize=10)

# Títulos e rótulos
plt.title('Quantidade de Empresas por Status')
plt.xlabel('Status')
plt.ylabel('Número de Empresas')

# Ajustar a rotação das labels no eixo X para facilitar a leitura
plt.xticks(rotation=45, ha='right')  # Rotaciona as labels no eixo X
plt.tight_layout()  # Ajusta o layout para evitar sobreposição
plt.show()

# Gráfico 2: Evolução das Fases ao longo do tempo
# Garantir que a coluna 'Data de Emissão' esteja no formato de data
df['Data de Emissão'] = pd.to_datetime(df['Data de Emissão'], errors='coerce')

# Criar o gráfico de linha para as fases
plt.figure(figsize=(12, 6))

# Plotando Fase 1
plt.plot(df['Data de Emissão'], df['Fase 1'], label='Fase 1')

# Plotando Fase 2
plt.plot(df['Data de Emissão'], df['Fase 2'], label='Fase 2')

# Adicionando título e rótulos
plt.title('Evolução das Fases ao Longo do Tempo')
plt.xlabel('Data de Emissão')
plt.ylabel('Fase')

# Adicionar legenda
plt.legend()

# Exibir o gráfico
plt.xticks(rotation=45)  # Rotaciona as labels do eixo X para melhor legibilidade
plt.tight_layout()  # Ajuste de layout para evitar sobreposição
plt.show()

