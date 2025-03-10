import re

# Função para formatar os CNPJs
def formatar_cnpjs(cnpjs):
    # Regex para remover os pontos, barra e traço
    cnpjs_formatados = [re.sub(r'\D', '', cnpj) for cnpj in cnpjs]
    return ",".join(cnpjs_formatados)

# Exemplo de lista de CNPJs
cnpjs = [
    "00.075.112/0001-01",
    "01.234.567/0001-89",
    "23.456.789/0001-12"
]

# Chamando a função
resultado = formatar_cnpjs(cnpjs)
print(resultado)
