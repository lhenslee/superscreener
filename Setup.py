import cx_Freeze
import csv
import decimal
import get_google
import pandas 
import tkinter
import save_tickers
import screener_settings
import os
import numpy

base = None

##if sys.platform == 'win32':
##    base = 'Win32GUI'

executables = [cx_Freeze.Executable('SuperScreener.py',base=base,icon='rari.ico')]

cx_Freeze.setup(
    name = 'Super Screener',
    options = {'build_exe': {'packages':['tkinter','decimal','csv','get_google','save_tickers','screener_settings','os','np'],'include_files':{'rari.ico'}}},
    version = '0.01',
    description = 'Screener for stocks in the past',
    executables = executables
    )
