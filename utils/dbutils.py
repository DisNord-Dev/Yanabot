import json
import logging
import mysql.connector
with open('config.json', 'r') as fichier:
        config = json.load(fichier)

def init_connection():
    mydb = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    passwd=config['mysql']['passwd'],
    database=config['mysql']['dbname']
    )
    return mydb

def close_connection(mydb):
    return mydb.close()
