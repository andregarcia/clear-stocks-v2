
import re
from datetime import datetime
from tika import parser
import os

from src.model.parsed_file import ParsedFile
from src.model.transaction import Transaction


def parse_operations_info(text):
    m = re.search('''Data pregão.*?([0-9]{2}/[0-9]{2}/[0-9]{4})''', text, re.DOTALL)
    if not m:
        raise Exception("Could not parse operations info")

    date = m.group(1)
    date_spl = date.split('/')
    parsed_date = datetime(day=int(date_spl[0]), month=int(date_spl[1]), year=int(date_spl[2]))
    return { 'data' : date, 'parsed_date' : parsed_date }


def parse_float(value):
    return float(value.replace('.', '').replace(',', '.'))


def parse_financial_summary(text):
    m = re.search('''([0-9\.]+,[0-9]{2})Total CBLC [DC]\s+?([0-9\.]+,[0-9]{2})Valor líquido das operações [DC]\s+?([0-9\.]+,[0-9]{2})Taxa de liquidação [DC]\s+?([0-9\.]+,[0-9]{2})Taxa de Registro [DC]\s+?([0-9\.]+,[0-9]{2})Total Bovespa / Soma [DC]\s+?([0-9\.]+,[0-9]{2})Taxa de termo/opções [DC]\s+?([0-9\.]+,[0-9]{2})Taxa A\.N\.A\. [DC]\s+?([0-9\.]+,[0-9]{2})Emolumentos [DC]\s+?([0-9\.]+,[0-9]{2})Total Custos / Despesas [DC]\s+?([0-9\.]+,[0-9]{2})Taxa Operacional [DC]\s+?([0-9\.]+,[0-9]{2})Execução\s+?([0-9\.]+,[0-9]{2})Taxa de Custódia\s+?([0-9\.]+,[0-9]{2})Impostos\s+?([0-9\.]+,[0-9]{2})I\.R\.R\.F\. s/ operações, base R\$[0-9\.]+,[0-9]{2}\s*[DC]{0,1}\s*?\s+?([0-9\.]+,[0-9]{2})Outros [DC]\s+?([0-9\.]+,[0-9]{2})Líquido para [0-9]{2}/[0-9]{2}/[0-9]{4} [DC]''', text, re.DOTALL)
    if not m:
        raise Exception("Could not parse financial summary")

    d = {}
    d['clearing'] = {}
    d['clearing']['valor_liquido_das_operacoes'] = m.group(2)
    d['clearing']['taxa_de_liquidacao'] = m.group(3)
    d['clearing']['taxa_de_registro'] = m.group(4)
    d['clearing']['total'] = m.group(1)

    d['bolsa'] = {}
    d['bolsa']['taxa_de_termo'] = m.group(6)
    d['bolsa']['taxa_ana'] = m.group(7)
    d['bolsa']['taxa_emolumentos'] = m.group(8)
    d['bolsa']['total'] = m.group(5)

    d['operacionais'] = {}
    d['operacionais']['total'] = m.group(9)
    d['operacionais']['taxa_operacional'] = m.group(10)
    d['operacionais']['execucao'] = m.group(11)
    d['operacionais']['taxa_custodia'] = m.group(12)
    d['operacionais']['impostos'] = m.group(13)
    d['operacionais']['irrf_sobre_operacoes'] = m.group(14)
    d['operacionais']['outros'] = m.group(15)
    d['liquido'] = m.group(16)
    return d


def parse_deal_summary(text):
    m = re.search('''([0-9\.]+,[0-9]{2}[\s]+)([0-9\.]+,[0-9]{2}[\s]+)([0-9\.]+,[0-9]{2}[\s]+)([0-9\.]+,[0-9]{2}[\s]+)([0-9\.]+,[0-9]{2}[\s]+)([0-9\.]+,[0-9]{2}[\s]+)([0-9\.]+,[0-9]{2}[\s]+)([0-9\.]+,[0-9]{2}[\s]+)\nResumo dos Negócios\nDebêntures\nVendas à vista\nCompras à vista\nOpções - compras\nOpções - vendas\nOperações à termo\nValor das oper\. c/ títulos públ\. \(v\. nom\.\)\nValor das operações\s+Especificações diversas''', text, re.DOTALL)
    if not m:
        raise Exception("Could not parse deal_summary")

    debentures = m.group(1).strip()
    vendas_a_vista = m.group(2).strip()
    compras_a_vista = m.group(3).strip()
    opcoes_compras = m.group(4).strip()
    opcoes_vendas = m.group(5).strip()
    operacoes_a_termo = m.group(6).strip()
    valor_das_operacoes_nominal = m.group(7).strip()
    valor_das_operacoes = m.group(8).strip()
    return {'debentures' : debentures,
            'vendas_a_vista' : vendas_a_vista,
            'compras_a_vista' : compras_a_vista,
            'opcoes_compras' : opcoes_compras,
            'opcoes_vendas' : opcoes_vendas,
            'operacoes_a_termo' : operacoes_a_termo,
            'valor_das_operacoes_nominal' : valor_das_operacoes_nominal,
            'valor_das_operacoes' : valor_das_operacoes}


def parse_stocks_operations(text, transaction_date):
    m = re.search('''Negócios realizados\nQ Negociação C/V Tipo mercado Prazo Especificação do título Obs\. \(\*\) Quantidade Preço / Ajuste Valor Operação / Ajuste D/C(.*?)NOTA DE NEGOCIAÇÃO''', text, re.DOTALL)
    if not m:
        raise Exception(f"Could not parse stocks operations")

    operations = m.group(1)
    operations = operations.strip()
    operation_lines = operations.split('\n')
    parsed_ops = []
    for line in operation_lines:
        if not line:
            continue
        m_op = re.search('^(1-BOVESPA) ([CV]) ([A-Z]+) ([A-Za-z0-9\s\.\/]+?)\s*(\s[2#8DFBACPHXYLTI]\s)?\s*([\.0-9]+) ([0-9\.]+,[0-9]{2}) ([0-9\.]+,[0-9]{2}) ([DC])', line)
        if not m_op:
            raise Exception(f"Could not parse operation line: {line}")

        negociacao = m_op.group(1)
        c_v = m_op.group(2)
        if c_v == 'C':
            c_v = 'COMPRA'
        elif c_v == 'V':
            c_v = 'VENDA'
        else:
            raise Exception(f"Valor de c/v invalido {c_v}")
        tipo_mercado = m_op.group(3)
        prazo = ''
        titulo_orig = m_op.group(4)
        titulo_orig = re.sub('\s+', ' ', titulo_orig)
        tokens = titulo_orig.split()

        titulo = tokens[0]
        siglas_to_keep = ['ON', 'PN', 'PNA']
        for token in tokens:
            if token in siglas_to_keep:
                titulo += ' ' + token


        obs = m_op.group(5).strip() if m_op.group(5) else None
        quantitdade = m_op.group(6).replace('.', '')
        preco = m_op.group(7)
        valor_operacao = m_op.group(8)
        d_c = m_op.group(9)
        if d_c not in ('D', 'C'): raise Exception("Error parsing stocks operation. Unexpected value points to a wrong parsing")
        parsed_ops.append(Transaction(negociacao, c_v, tipo_mercado, prazo, titulo, obs, quantitdade, preco, valor_operacao, d_c, transaction_date))
    return parsed_ops


def parse_text(text):
    text = text.strip()
    info = parse_operations_info(text)
    transactions = parse_stocks_operations(text, info['parsed_date'])
    transactions = sorted(transactions, key = lambda x: x.date)
    deals_summary = parse_deal_summary(text)
    financial_summary = parse_financial_summary(text)
    return ParsedFile(info['parsed_date'], transactions, deals_summary, financial_summary)


def convert_pdf_to_txt(path):
    rawText = parser.from_file(path)
    parsed = parse_text(rawText['content'])
    return parsed


def list_files(path):
    files = []
    for file in os.listdir(path):
        if re.match('NotaNegociacao_.*.pdf', file):
            files.append(os.path.join(path, file))
    return files


def parse_all_files(path):
    files = list_files(path)
    parsed_files = []
    for file in files:
        print(f"Processing file {file}")
        parsed_files.append(convert_pdf_to_txt(file))

    return parsed_files