import sqlite3
import pandas as pd
import warnings
import numpy as np
from types import *

warnings.filterwarnings('ignore')

class DBManager:
    path: str = "main.db"
    conn: sqlite3.Connection = None
    
    def __init__(self):
        pass
    
    def connect(self):
        self.conn = sqlite3.connect("main.db")

class Migration:
    conn: sqlite3.Connection = None
    
    def __init__(self):
        self.conn = DBManager().connect()
         
        

if __name__ == "main":
    pass