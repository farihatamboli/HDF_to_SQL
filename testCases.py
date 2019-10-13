#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:56:14 2019

@author: Tamboli
"""

from __future__ import print_function
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import errorcode
config = {
    'user': 'root',
    'password': '*****',
    'host': '127.0.0.1',
    'database': 'orbitdata',
    #'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
DB_NAME = 'orbitdata'
#connect to database


# =============================================================================
# These are some different test cases of possible separations we want.
# =============================================================================

#Create new table with all shots that did not go out of bounds
def create_table_boundsTrue(cursor): #create table
    try:
        cursor.execute(
                "CREATE TABLE boundsTrue (shot INT (5), bounds INT (10) NOT NULL, PRIMARY KEY(shot) )")
    except mysql.connector.Error as err:
        print("Failed creating table: ".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Table {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_table_boundsTrue(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)
        
def boundsTrue(cursor):
    create_table_boundsTrue(cursor)
    cursor.execute("SELECT * FROM bounds WHERE bounds = 30000 ")
    result = cursor.fetchall()
    for x in result:
        print(str(x[0]) + " " + str(x[1]))

        insert = """ INSERT INTO `boundsTrue`
                          (`shot`, `bounds`) VALUES (%s,%s)"""
        values = (str(x[0]) , str(x[1]))
        cursor.execute(insert, values)
        cnx.commit()
        return x

# =============================================================================
# Return the radius, iteration, velocity of specific shot numbers. In this case, 
# return the I R V for all boundsTrue
# =============================================================================

#Create new table for this new relational data
def create_table_boundsTrueR(cursor): #create table
    try:
        cursor.execute(
                "CREATE TABLE boundsTrueR (shot INT (5), bounds INT (10) NOT NULL, PRIMARY KEY(shot) )")
    except mysql.connector.Error as err:
        print("Failed creating table: ".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Table {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_table_boundsTrue(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)
        
def boundsTrueR(cursor):
    #create_table_boundsTrueR(cursor)
    cursor.execute("USE orbitdata; SELECT * INTO boundsTrueR FROM boundsTrue LEFT JOIN radius ON boundsTrue.shot = radius.shot; ", multi=True)
    result = cursor.fetchall()
    for x in result:
         print(str(x[0]) + " " + str(x[1]))
#        insert = """ INSERT INTO `boundsTrue`
#                           (`shot`, `bounds`) VALUES (%s,%s)"""
#         values = (str(x[0]) , str(x[1]))
#         cursor.execute(insert, values)
# =============================================================================
    cnx.commit()

def createChart(cursor):
    cursor.execute("SELECT * FROM bounds WHERE bounds = 30000 ")
    result = cursor.fetchall()
    for x in result:
        print(str(x[0]) + " " + str(x[1]))
    plt.plot(x[0], x[1])
    plt.show()
def Main(cursor):
   boundsTrueCount = boundsTrue(cursor)
  # boundsTrueR(cursor)
   createChart(cursor)
   print("true bounds count = " + boundsTrueCount)

print (__name__)

if __name__ == "__main__":
   Main(cursor)
    
