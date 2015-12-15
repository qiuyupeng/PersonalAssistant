import os
import sys
#parent dir of current folder
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#put PARENT_DIR in search path
sys.path.append(PARENT_DIR)

from StockDataPipe.googleFinancePull import stockPriceWritter

stock_writter = stockPriceWritter()

stock_writter.query()

