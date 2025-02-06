import os
import base64
import json
import requests
import xml.etree.ElementTree as eT
from time import sleep
from constants import URL_REQUEST, URL_TRANSMIT, URL_SUPPORT, API_SECRETS, ACCOUNTANT_CODE, CNPJS_LIST, read_keys


cnpjs_com_erro = []

def generate_data(modulo, caminho, periodo, client_code):
    read_keys()
    header = {
        "Authorization": f"Bearer {API_SECRETS.get('accessToken')}",
        "content-type": "application/json",
        "jwt_token": API_SECRETS.get('jwtToken')
    }
    data = {
        "contratante": {
            "numero": ACCOUNTANT_CODE,
            "tipo": 2
        },
        "autorPedidoDados": {
            "numero": ACCOUNTANT_CODE,
            "tipo": 2
        },
        "contribuinte": {
            "numero": client_code,
            "tipo": 2
        },
    }
    url = ''

    if modulo == 'sit_fiscal':
        data["pedidoDados"] = {
            "idSistema": "SITFIS",
            "idServico": "SOLICITARPROTOCOLO92",
            "versaoSistema": "2.0",
            "dados": ""
        }

        # Solicitar protocolo do relatório de situação fiscal
        support = requests.post(URL_SUPPORT, data=json.dumps(data), headers=header)
        print('-----------------------------------------')
        print(support.json())
        print('-----------------------------------------')

        if support.status_code == 304:
            value = support.headers.get('etag').split(":", 1)[1].strip('"')
            wait = 0
        else:
            content = json.loads(support.json().get('dados'))
            value = content.get('protocoloRelatorio')
            wait = int(content.get('tempoEspera')) / 100

        data["pedidoDados"]["idServico"] = "RELATORIOSITFIS92"
        data["pedidoDados"]["versaoSistema"] = "2.0"
        data["pedidoDados"]["dados"] = '{{ "protocoloRelatorio":  "{}" }}'.format(value)

        url = URL_TRANSMIT

        sleep(wait)

    elif modulo == 'pgdas':
        data["pedidoDados"] = {
            "idSistema": "PGDASD",
            "idServico": "GERARDAS12",
            "versaoSistema": "1.0",
            "dados": '{{ "periodoApuracao": "{}" }}'.format(periodo)
        }
        url = URL_TRANSMIT   

    elif modulo == 'rel_pagamentos':
        data["pedidoDados"] = {
            "idSistema": "PAGTOWEB",
            "idServico": "PAGAMENTOS71",
            "dados": '{{ "intervaloDataArrecadacao": {{"dataInicial": "{}", "dataFinal": "{}"}}, "primeiroDaPagina": 0,"tamanhoDaPagina": 100 }}'.format(periodo[0], periodo[1]) # noqa
        }

        url = URL_REQUEST


    elif modulo == 'PARCSN':
        data["pedidoDados"] = {
            "idSistema": "PARCSN",
            "idServico": "GERARDAS161",
            "versaoSistema": "1.0",
            "dados": '{{ "parcelaParaEmitir": {} }}'.format(periodo)
       }

        url = URL_TRANSMIT

    elif modulo == 'PGMEI':
        data["pedidoDados"] = {
            "idSistema": "PGMEI",
            "idServico": "GERARDASPDF21",
            "versaoSistema": "1.0",
            "dados": '{{ "periodoApuracao": {} }}'.format(periodo)
       }
        
        url = URL_TRANSMIT

    res = requests.post(url, data=json.dumps(data), headers=header)
    print(f'Status code da requisição {modulo}: {res.status_code}')
    print(f"Resposta a requisição {modulo}:", res.json())
    print('---------------------------------------')

    if res.status_code == 200:
        if '.xml' in caminho:
            documentos = json.loads(json.loads(res.content.decode('utf-8')).get('dados'))

            # elemento root
            principal = eT.Element("pagamentos")

            for documento in documentos:
                doc = eT.SubElement(principal, "pagamento")

                numero_documento = eT.SubElement(doc, "numeroDocumento")
                numero_documento.text = str(documento["numeroDocumento"])

                tipo = eT.SubElement(doc, "tipo")

                codigo_tipo = eT.SubElement(tipo, "codigo")
                codigo_tipo.text = str(documento["tipo"]["codigo"])
                descricao_tipo = eT.SubElement(tipo, "descricao")
                descricao_tipo.text = str(documento["tipo"]["descricao"])
                descricao_abreviada_tipo = eT.SubElement(tipo, "descricaoAbreviada")
                descricao_abreviada_tipo.text = str(documento["tipo"]["descricaoAbreviada"])

                periodo_apuracao = eT.SubElement(doc, "periodoApuracao")
                periodo_apuracao.text = str(documento["periodoApuracao"])
                data_arrecadacao = eT.SubElement(doc, "dataArrecadacao")
                data_arrecadacao.text = str(documento["dataArrecadacao"])
                data_vencimento = eT.SubElement(doc, "dataVencimento")
                data_vencimento.text = str(documento["dataVencimento"])

                receita = eT.SubElement(doc, "receitaPrincipal")

                codigo_receita = eT.SubElement(receita, "codigo")
                codigo_receita.text = str(documento["receitaPrincipal"]["codigo"])
                descricao_receita = eT.SubElement(receita, "descricao")
                descricao_receita.text = str(documento["receitaPrincipal"]["descricao"])
                extensao_receita = eT.SubElement(receita, "extensaoReceita")
                extensao_receita.text = str(documento["receitaPrincipal"]["extensaoReceita"])

                referencia = eT.SubElement(doc, "referencia")
                referencia.text = str(documento["referencia"])
                valor_total = eT.SubElement(doc, "valorTotal")
                valor_total.text = str(documento["valorTotal"])
                valor_principal = eT.SubElement(doc, "valorPrincipal")
                valor_principal.text = str(documento["valorPrincipal"])
                valor_multa = eT.SubElement(doc, "valorMulta")
                valor_multa.text = str(documento["valorMulta"])
                valor_juros = eT.SubElement(doc, "valorJuros")
                valor_juros.text = str(documento["valorJuros"])
                valor_saldo_total = eT.SubElement(doc, "valorSaldoTotal")
                valor_saldo_total.text = str(documento["valorSaldoTotal"])
                valor_saldo_principal = eT.SubElement(doc, "valorSaldoPrincipal")
                valor_saldo_principal.text = str(documento["valorSaldoPrincipal"])
                valor_saldo_multa = eT.SubElement(doc, "valorSaldoMulta")
                valor_saldo_multa.text = str(documento["valorSaldoMulta"])
                valor_saldo_juros = eT.SubElement(doc, "valorSaldoJuros")
                valor_saldo_juros.text = str(documento["valorSaldoJuros"])

                desmembramentos = eT.SubElement(doc, "desmembramentos")

                for desmembramento in documento["desmembramentos"]:
                    item_desmembramento = eT.SubElement(desmembramentos,
                                                        "desmembramento-" + desmembramento["sequencial"])

                    desmembramento_receita = eT.SubElement(item_desmembramento, "receitaPrincipal")

                    desmembramento_receita_codigo = eT.SubElement(desmembramento_receita, "codigo")
                    desmembramento_receita_codigo.text = str(desmembramento["receitaPrincipal"]["codigo"])
                    desmembramento_receita_descricao = eT.SubElement(desmembramento_receita, "descricao")
                    desmembramento_receita_descricao.text = str(desmembramento["receitaPrincipal"]["descricao"])
                    desmembramento_receita_extensao = eT.SubElement(desmembramento_receita, "extensaoReceita")
                    desmembramento_receita_extensao.text = str(desmembramento["receitaPrincipal"]["extensaoReceita"])

                    desmembramento_periodo = eT.SubElement(item_desmembramento, "periodoApuracao")
                    desmembramento_periodo.text = str(desmembramento["periodoApuracao"])
                    desmembramento_vencimento = eT.SubElement(item_desmembramento, "dataVencimento")
                    desmembramento_vencimento.text = str(desmembramento["dataVencimento"])
                    desmembramento_total = eT.SubElement(item_desmembramento, "valorTotal")
                    desmembramento_total.text = str(desmembramento["valorTotal"])
                    desmembramento_principal = eT.SubElement(item_desmembramento, "valorPrincipal")
                    desmembramento_principal.text = str(desmembramento["valorPrincipal"])
                    desmembramento_multa = eT.SubElement(item_desmembramento, "valorMulta")
                    desmembramento_multa.text = str(desmembramento["valorMulta"])
                    desmembramento_juros = eT.SubElement(item_desmembramento, "valorJuros")
                    desmembramento_juros.text = str(desmembramento["valorJuros"])

                    desmembramento_saldo_total = eT.SubElement(item_desmembramento, "valorSaldoTotal")
                    desmembramento_saldo_total.text = str(desmembramento["valorSaldoTotal"])
                    desmembramento_saldo_principal = eT.SubElement(item_desmembramento, "valorSaldoPrincipal")
                    desmembramento_saldo_principal.text = str(desmembramento["valorSaldoPrincipal"])
                    desmembramento_saldo_multa = eT.SubElement(item_desmembramento, "valorSaldoMulta")
                    desmembramento_saldo_multa.text = str(desmembramento["valorSaldoMulta"])
                    desmembramento_saldo_juros = eT.SubElement(item_desmembramento, "valorSaldoJuros")
                    desmembramento_saldo_juros.text = str(desmembramento["valorSaldoJuros"])

                    desmembramento_cib = eT.SubElement(item_desmembramento, "cib")
                    desmembramento_cib.text = str(desmembramento["cib"])

            tree = eT.ElementTree(principal)
            tree.write(caminho, encoding="utf-8", xml_declaration=True)
            return True
        
        else:
            try:
                pdf = json.loads(res.json().get('dados')).get("declaracao").get("pdf")
            except AttributeError:
                pdf = json.loads(res.json().get('dados')).get('pdf')


            diretorio = os.path.dirname(caminho)
            # Se o diretório não existir, crie-o
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)

            if not os.path.isfile(caminho):
                open(caminho, 'w').close()
            
            try:
                with open(caminho, "wb") as f:
                    f.write(base64.b64decode(pdf))
                    print(f'Decodificação relatório {client_code} feita com sucesso')
                return True
            except Exception as e:
                print(f"Erro ao decodificar o arquivo para o CNPJ {client_code}: {e}")
                # Adiciona o CNPJ à lista de falhas
                cnpjs_com_erro.append(client_code)
                return False
    else:
        # Em caso de falha na requisição
        cnpjs_com_erro.append(client_code)
        return False