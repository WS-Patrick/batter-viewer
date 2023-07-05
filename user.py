# import mysql.connector
from configparser import ConfigParser
# cnx: mysql.connector.connect = None

def login (userName, password):
    if userName == "1111":
        if password =="1111":
            return True
        else:
            False
    else:
        return False
