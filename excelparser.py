import xlrd
import glob
from datetime import datetime
from os import devnull
from datetime import date, datetime

def build_pedidos(pedidos, skipped, pedidos_filename):
    """Given an existing 'pedidos' dict, add or replace pedidos to it.
    Only the date is saved.

    Skipped pedidos are added to 'skipped' set
    """
    pedidos_book = xlrd.open_workbook(pedidos_filename, logfile=open(devnull, 'w'))
    pedidos_sheet = pedidos_book.sheet_by_index(0)

    label = pedidos_sheet.cell(0, 1).value[:3]
    if not label:
        label = pedidos_sheet.cell(0, 2).value[:3]
        
    pedidos_rows = pedidos_sheet.nrows

    # column numbers
    NUMERO = 1
    CLIENTE = 2
    DATA = 5

    for pedido_row in range(pedidos_rows):
        numeroCellValue = pedidos_sheet.cell(pedido_row, NUMERO).value
                
        if isinstance(numeroCellValue, str):
            continue

        try:
            numero = int(numeroCellValue)
        except ValueError:
            response_err += "Could not read numero {}. Skipping\n".format(numeroCellValue)
            continue

        pedido_cliente = pedidos_sheet.cell(pedido_row, CLIENTE).value
        if pedido_cliente.startswith("UNIAO BRINDES IMPORT") or pedido_cliente.startswith("PONTUAL EXPORT"):
            print("skipping", numero, "uniao or ptl")
            skipped.add(label + str(numero))
            continue
        
        try:
            dataValue = pedidos_sheet.cell(pedido_row, DATA).value
            data = datetime.strptime(dataValue, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            dataValue = pedidos_sheet.cell(pedido_row, DATA+1).value
            data = datetime.strptime(dataValue, "%d/%m/%Y").strftime("%Y-%m-%d")
            
        pedidos[label+str(numero)] = data

        
def build_itens(itens, pedidos, skipped, itens_filename):
    itens_book = xlrd.open_workbook(itens_filename, logfile=open(devnull, 'w'))
    itens_sheet = itens_book.sheet_by_index(0)
    
    label = itens_sheet.cell(0, 1).value[:3]
    if not label:
        label = itens_sheet.cell(0, 2).value[:3]

    itens_rows = itens_sheet.nrows
    NUMERO = 1
    CODIGO_PRODUTO = 2
    QTDE = 7

    for item_row in range(itens_rows):
        numeroCellValue = itens_sheet.cell(item_row, NUMERO).value
        
        if isinstance(numeroCellValue, str):
            continue

        try:
            numero = int(numeroCellValue)
        except ValueError:
            continue

        pedido_label = label + str(numero)

        produtoCellValue = itens_sheet.cell(item_row, CODIGO_PRODUTO).value
        if isinstance(produtoCellValue, str):
            codigoProduto = produtoCellValue
        else:
            codigoProduto = str(int(produtoCellValue))

        if codigoProduto == "DESC":
            continue

        if codigoProduto == "140975":
            codigoProduto = "140975E"

        qtdeCellValue = itens_sheet.cell(item_row, QTDE).value
        if isinstance(qtdeCellValue, str):
            continue
        qtde = int(qtdeCellValue)

        k = pedido_label + "_" + codigoProduto

        try:
            itens[k] = (pedidos[pedido_label], codigoProduto, str(qtde))
        except KeyError:
            # pedido not found because it was skipped for being uniao
            if pedido_label not in skipped:
                print(pedido_label, "does not exist, was the pedido loaded?")

                
def parse_sales(pedidos_filename, itens_filename, output_filename):
    """Given the filenames of pedidos (numero sintetico) and
    itens (produto analitico), return a list of produto, date and quantity rows.

    Sample output:
    [[datetime(2019, 9, 2, 0, 0), "137350A", 480],
     [datetime(2019, 8, 28, 0, 0), "143135", 20],
    ]
    """
    
    pedidos_book = xlrd.open_workbook(pedidos_filename)
    itens_book = xlrd.open_workbook(itens_filename)

    pedidos_sheet = pedidos_book.sheet_by_index(0)
    itens_sheet = itens_book.sheet_by_index(0)

    label = pedidos_sheet.cell(0, 1).value[:3]

    print(label)

    pedidos_rows = pedidos_sheet.nrows
    pedidos = {}
    # column numbers
    NUMERO = 1
    CLIENTE = 2
    DATA = 5

    itens_rows = itens_sheet.nrows
    itens = []
    CODIGO_PRODUTO = 2
    QTDE = 7

    for pedido_row in range(pedidos_rows):
        numeroCellValue = pedidos_sheet.cell(pedido_row, NUMERO).value
                
        if isinstance(numeroCellValue, str):
            continue

        try:
            numero = int(numeroCellValue)
        except ValueError:
            response_err += "Could not read numero {}. Skipping\n".format(numeroCellValue)
            continue

        nomeCliente = pedidos_sheet.cell(pedido_row, CLIENTE).value
        dataValue = pedidos_sheet.cell(pedido_row, DATA).value
        data = datetime.strptime(dataValue, "%d/%m/%Y").strftime("%Y-%m-%d")

        pedidos[label+str(numero)] = (data, nomeCliente)

    for item_row in range(itens_rows):
        numeroCellValue = itens_sheet.cell(item_row, NUMERO).value

        if isinstance(numeroCellValue, str):
            continue

        try:
            numero = int(numeroCellValue)
        except ValueError:
            continue

        pedido_label = label + str(numero)
        pedido_cliente = pedidos[pedido_label][1]
        pedido_data = pedidos[pedido_label][0]

        if pedido_cliente.startswith("UNIAO BRINDES IMPORT") or pedido_cliente.startswith("PONTUAL EXPORT"):
            pass
        else:
            produtoCellValue = itens_sheet.cell(item_row, CODIGO_PRODUTO).value
            if isinstance(produtoCellValue, str):
                codigoProduto = produtoCellValue
            else:
                codigoProduto = str(int(produtoCellValue))

            if codigoProduto == "DESC":
                continue

            if codigoProduto == "140975":
                codigoProduto = "140975E"

            qtdeCellValue = itens_sheet.cell(item_row, QTDE).value
            if isinstance(qtdeCellValue, str):
                continue
            qtde = int(qtdeCellValue)

            itens.append((pedido_data, codigoProduto, str(qtde)))
            
    # generate CSV
    with open(output_filename, 'w', encoding="utf-8") as outf:
        print("data,codigo,qtde", file=outf)
        for i in itens:
            print(",".join(i), file=outf)
            
    print("Wrote", output_filename)


def write_date_prod_csv(itens, output_filename):
    with open(output_filename, 'w', encoding="utf-8") as outf:
        print("data,codigo,qtde", file=outf)
        for i in itens.values():
            print(",".join(i), file=outf)


def compile_xls():
    DIR = "data"

    companies = ["ptl", "uni"]

    pedidos = {}
    skipped = set()
    itens = {}
    
    # numsint
    for label in companies:
        filenames = glob.glob(DIR + "/numsint/" + label + "/*.xls")
        for filename in filenames:
            print("reading pedido", filename)
            build_pedidos(pedidos, skipped, filename)

    # prodan
    for label in companies:
        filenames = glob.glob(DIR + "/prodan/" + label + "/*.xls")
        for filename in filenames:
            print("reading itens", filename)
            build_itens(itens, pedidos, skipped, filename)

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    write_date_prod_csv(itens, DIR + "/compiled_" + timestamp + ".csv")
