# Sales Analysis

## Requirements

* Python 3
* NumPy
* Pandas
* xlrd
* pyautogui

## Procedure

1. Call variations of `get_sales()`, `get_prod_ptl()` and `get_prod_uni()` from `collectdata.py` (run from the command line). Make sure to have the right management window open.

2. In an interactive shell, call `compile_xls()`. Change the `DIR` variable if needed.

3. Check whether there are gaps in the pedidos dates with `skipped_days()` in `checkpedidos.py`