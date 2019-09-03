import xlrd
from datetime import date

def parse_sales(pedidos_filename, itens_file):
    with open(pedidos_filename) as pedidos_file, open(itens_file) as itens_file:
        pedidos_book = xlrd.open_workbook(file_contents=pedidos_file)
        itens_book = xlrd.open_workbook(file_contents=itens_file)

        pedidos_sheet = pedidos_book.sheet_by_index(0)
        itens_sheet = itens_book.sheet_by_index(0)

        print()
