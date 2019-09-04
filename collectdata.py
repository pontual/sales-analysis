import sys
import subprocess
from time import sleep
import pyautogui
from pyautogui import moveTo, click, typewrite

pyautogui.PAUSE = 0.25
DEST_DIR = "c:\\Users\\Heitor\\Desktop\\code\\sales-analysis\\data"

def set_dates(year, month):
    DAY_X = 404
    MONTH_X = 428
    YEAR_X = 456
    TOP_Y = 231
    BOTTOM_Y = 269

    if month == 12:
        end_month = 1
        end_year = year + 1
    else:
        end_month = month + 1
        end_year = year
        
    click(MONTH_X, TOP_Y)
    typewrite(str(month))

    click(YEAR_X, TOP_Y)
    typewrite(str(year))

    click(DAY_X, BOTTOM_Y)
    typewrite("01")

    click(MONTH_X, BOTTOM_Y)
    typewrite(str(end_month))

    click(YEAR_X, BOTTOM_Y)
    typewrite(str(end_year))

    
def save_num_sint(year, month, label):
    fname = "{}\\numsint\\{}\\numsint_{}_{:02d}".format(DEST_DIR, label, year, month)
    
    subprocess.run(r'winactivateloja.exe')
    
    click(410, 33)
    moveTo(458, 137)
    sleep(0.5)

    moveTo(587, 137)
    moveTo(615, 252)
    sleep(0.9)

    moveTo(705, 255)
    sleep(0.5)
    click(705, 266)
    sleep(1)

    for i in range(6):
        typewrite("\n")

    sleep(1)

    set_dates(year, month)
    typewrite("\n")

    sleep(5)
    click(84, 49)
    sleep(0.5)
    typewrite(fname)
    sleep(0.5)
    typewrite("\n")

    sleep(2)
    
    click(1277, 3)
    sleep(2)


def save_prod_an(year, month, label):
    fname = "{}\\prodan\\{}\\prodan_{}_{:02d}".format(DEST_DIR, label, year, month)

    subprocess.run(r'winactivateloja.exe')

    click(410, 33)
    moveTo(458, 137)
    sleep(0.5)

    moveTo(587, 137)
    moveTo(613, 188)
    sleep(0.9)

    moveTo(705, 190)
    sleep(0.5)
    click(705, 190)
    sleep(1)

    click(317, 226)
    
    for i in range(5):
        typewrite("\n")

    sleep(1)

    set_dates(year, month)
    typewrite("\n")

    sleep(10)
    click(84, 49)
    sleep(0.5)
    typewrite(fname)
    sleep(0.5)
    typewrite("\n")

    sleep(3)
    
    click(1277, 3)
    sleep(2)
    

def get_sales():
    # Uniao
    uni_num_sint = """
    for month in range(8, 13):
        save_num_sint(2017, month, 'uni')
    
    for month in range(1, 13):
        save_num_sint(2018, month, 'uni')

    for month in range(1, 9):
        save_num_sint(2019, month, 'uni')
    """    


def get_prod_ptl():
    for year in range(2015, 2019):
        for month in range(1, 13):
            save_prod_an(year, month, "ptl")

    for month in range(1, 9):
        save_prod_an(2019, month, "ptl")


def get_prod_uni():
    for month in range(8, 13):
        save_prod_an(2017, month, 'uni')
    
    for month in range(1, 13):
        save_prod_an(2018, month, 'uni')

    for month in range(1, 9):
        save_prod_an(2019, month, 'uni')

        
if __name__ == "__main__":
    # get_prod_uni()
    print("Edit the source to save files from the management software")


