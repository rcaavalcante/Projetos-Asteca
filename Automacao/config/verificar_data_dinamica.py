import datetime
import re

def verificar_data_mes_ano(driver):
    # Obtém a data atual
    data_atual = datetime.datetime.now()
    mes_ano_atual = data_atual.strftime('%m/%Y')  # Formato: MM/AAAA
    
    # Captura o texto da página inteira
    pagina_texto = driver.page_source
    
    # Procura por datas no formato DD/MM/YYYY ou MM/YYYY
    match = re.search(r'\b\d{2}/\d{4}\b', pagina_texto)  # Busca por MM/AAAA na página
    
    if match:
        data_encontrada = match.group(0)  # Formato: MM/YYYY
        # Comparar se o mês e o ano são os mesmos
        if data_encontrada == mes_ano_atual:
            return True
    return False