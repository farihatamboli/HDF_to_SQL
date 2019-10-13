#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 19:11:28 2019

@author: Tamboli
"""

from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
config = {
    'user': 'root',
    'password': '*****',
    'host': '127.0.0.1',
    'database': 'sys',
    #'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
#connect to database
def _connect():
    config = {
        'user': 'root',
        'password': '*****',
        'host': '127.0.0.1',
        'database': 'sys',
        #'raise_on_warnings': True,
    }
    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        if cnx:
            cnx.close()
    return cnx 

DB_NAME = 'orbitdata'
TABLES = {}

# =============================================================================
# TABLES['rValue'] = (
#     "CREATE TABLE `rValue` ("
#     "  `primary id` int(14) NOT NULL, AUTO_INCREMENT"
#     "  `particle id` int(10) NOT NULL AUTO_INCREMENT,"
#     "  `shot id` int(10) NOT NULL, AUTO_INCREMENT"
#     "  `valueR` decimal(14) NOT NULL,"
#     "  PRIMARY KEY (`primary id`)"
#     ") ENGINE=InnoDB")
# 
# TABLES['vValue'] = (
#     "CREATE TABLE `vValue` ("
#     "  `primary id` int(14) NOT NULL, AUTO_INCREMENT"
#     "  `particle id` int(10) NOT NULL AUTO_INCREMENT,"
#     "  `shot id` int(10) NOT NULL, AUTO_INCREMENT"
#     "  `valueV` decimal(14) NOT NULL,"
#     "  PRIMARY KEY (`primary id`)"
#     ") ENGINE=InnoDB")
# 
# TABLES['bounds'] = (
#     "CREATE TABLE `bounds` ("
#     "  `primary id` int(14) NOT NULL, AUTO_INCREMENT"
#     "  `particle id` int(10) NOT NULL AUTO_INCREMENT,"
#     "  `shot id` int(10) NOT NULL, AUTO_INCREMENT"
#     "  `inORout` int(1) NOT NULL,"
#     "  PRIMARY KEY (`primary id`)"
#     ") ENGINE=InnoDB")
# 
# TABLES['steps'] = (
#     "CREATE TABLE `steps` ("
#     "  `primary id` int(14) NOT NULL, AUTO_INCREMENT"
#     "  `particle id` int(10) NOT NULL AUTO_INCREMENT,"
#     "  `shot id` int(10) NOT NULL, AUTO_INCREMENT"
#     "  `timeStep` decimal(14) NOT NULL,"
#     "  PRIMARY KEY (`primary id`)"
#     ") ENGINE=InnoDB")
# =============================================================================

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)    
# =============================================================================
# for table_name in TABLES:
#     table_description = TABLES[table_name]
#     try:
#         print("Creating table {}: ".format(table_name), end='')
#         cursor.execute(table_description)
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("already exists.")
#         else:
#             print(err.msg)
#     else:
#         print("OK")
# =============================================================================



def create_tableV(cursor):
    try:
        cursor.execute(
                "CREATE TABLE velocity (shot INT (5) , timeStep INT (5), vX DECIMAL(55, 29), vY DECIMAL(55, 29), vZ DECIMAL(55, 29), PRIMARY KEY(shot, timeStep) )")
              # "CREATE TABLES {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating table: ".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Table {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)    


def create_tableR(cursor):
    try:
        cursor.execute(
                "CREATE TABLE radius (shot INT (5) , timeStep INT (5), rX DECIMAL(55, 29), rY DECIMAL(55, 29), rZ DECIMAL(55, 29), PRIMARY KEY(shot, timeStep) )")
              # "CREATE TABLES {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating table: ".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Table {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_tableR(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1) 
        
def create_tableI(cursor):
    try:
        cursor.execute(
                "CREATE TABLE iter (shot INT (5), iter INT (10) NOT NULL, PRIMARY KEY(shot) )")
              # "CREATE TABLES {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating table: ".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Table {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_tableR(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)    

def create_tableB(cursor):
    try:
        cursor.execute(
                "CREATE TABLE bounds (shot INT (5), bounds INT (10) NOT NULL, PRIMARY KEY(shot) )")
              # "CREATE TABLES {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating table: ".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Table {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_tableR(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1) 

def Main(cursor):
    create_database(cursor)   
    create_tableV(cursor)
    create_tableR(cursor)
    create_tableI(cursor)
    create_tableB(cursor)

print (__name__)

if __name__ == "__main__":
   Main(cursor)
