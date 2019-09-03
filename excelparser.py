import xlrd
from datetime import date, datetime

def parse_sales(pedidos_filename, itens_file):
    """Given the filenames of pedidos (numero sintetico) and
    itens (produto analitico), return a list of produto, date and quantity rows.

    Sample output:
    [[datetime(2019, 9, 2, 0, 0), "137350A", 480],
     [datetime(2019, 8, 28, 0, 0), "143135", 20],
    ]
    """
    
    with open(pedidos_filename) as pedidos_file, open(itens_file) as itens_file:
        pedidos_book = xlrd.open_workbook(file_contents=pedidos_file)
        itens_book = xlrd.open_workbook(file_contents=itens_file)

        pedidos_sheet = pedidos_book.sheet_by_index(0)
        itens_sheet = itens_book.sheet_by_index(0)

        print()

        
