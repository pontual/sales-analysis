import xlrd
from datetime import date, datetime

def parse_sales(pedidos_filename, itens_filename):
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
        data = datetime.strptime(dataValue, "%d/%m/%Y")

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
            print("Skipping Uniao/Pontual pedido", pedido_label)
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

            itens.append((pedido_data, codigoProduto, qtde))
    return itens
