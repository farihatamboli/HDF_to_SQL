#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:07:11 2019

@author: Tamboli
"""
from __future__ import print_function
#import numpy as np
import h5py
import os
#import sys
import mysql.connector
#from mysql.connector import errorcode
config = {
    'user': 'root',
    'password': 'BrynMawr',
    'host': '127.0.0.1',
    'database': 'orbitdata',
    #'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
#connect to database

# =============================================================================
# These are functions to read in the data from the HDF files. I have commented out
# the debugging print functions but still left them in there. Just like creating
# the database tables, it is possible to do these functions in one function using
# a dictionary. I just could not figure it out. 
# =============================================================================
def readB(datadir, input_file): 
    f = h5py.File(datadir+input_file, 'r')
    # List all groups
    #print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[0]
    # Get the data
    data = list(f[a_group_key])
    #print(data)
    return(data)
def readI(datadir, input_file):
    f = h5py.File(datadir+input_file, 'r')
    # List all groups
    #print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[1]
    # Get the data
    data = list(f[a_group_key])
    #print(data)
    return(data)
def readV(datadir, input_file):
    f = h5py.File(datadir+input_file, 'r')
    # List all groups
    #print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[2]
    # Get the data
    data = list(f[a_group_key])
    #print(data)
    return(data)
def readR(datadir, input_file):
    f = h5py.File(datadir+input_file, 'r')
    # List all groups
    #print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[3]
    # Get the data
    data = list(f[a_group_key])
    #print(data)
    return(data)
    
# =============================================================================
# These functions read the data and obtain it into the SQL database tables. 
# The HDF dataset comes in as a python list, which cannot be converted to MySQL
# datatype, so it has to be changed into a string then inserted into SQL. Again,
# these functions can probably be done in one function using a dictionary. 
# =============================================================================
def insertB(cursor, numFile, datadir, file_name):
    b = readB(datadir, file_name)
    add_bounds = "INSERT INTO bounds (shot, bounds) VALUES (%s, %s)"
    for x in b:
        data_bounds =  (numFile, str(x)) 
        cursor.execute(add_bounds, data_bounds)
    cnx.commit()
    print(cursor.rowcount, "record inserted.")  
def insertI(cursor, numFile, datadir, file_name):
    #HDF iter type was boolean. Could not figure out how to convert, so I just 
    #went to the bounds and determined 0 or 1 from there 
    b = readB(datadir, file_name)
    for x in b:
        if x == 30000: #0 is true, not out of bounds
            data_iter = (numFile, "0")
        else: #1 is fale, it is out of bounds
            data_iter = (numFile, "1")
    add_iter = "INSERT INTO iter (shot, iter) VALUES (%s, %s)"
    cursor.execute(add_iter, data_iter)
    cnx.commit()
    print(cursor.rowcount, "record inserted.")   
def insertR(cursor, numFile, datadir, file_name):
    r = readR(datadir, file_name)
    add_radius = "INSERT INTO radius (shot, timeStep, rX, rY, rZ) VALUES (%s, %s, %s, %s, %s)"
    count = 1
    for x in r:
        if(x[0]==0 and x[1]==0 and x[2]==0): #to not put in R rows after it went out of bounds
            data_radiusZ =  (numFile, count, str(x[0]), str(x[1]), str(x[2])) 
            count+=1
            cursor.execute(add_radius, data_radiusZ)
            break
        else:
            data_radius =  (numFile, count, str(x[0]), str(x[1]), str(x[2])) 
            count+=1
            cursor.execute(add_radius, data_radius)
    cnx.commit()
    print(cursor.rowcount, "record inserted.") 
    return count
def insertV(cursor, numFile, datadir, file_name, countR):
    v = readV(datadir, file_name)
    add_velocity = "INSERT INTO velocity (shot, timeStep, vX, vY, vZ) VALUES (%s, %s, %s, %s, %s)"
    count = 1
    while count <= countR:
        for x in v:
                data_velocity =  (numFile, count, str(x[0]), str(x[1]), str(x[2])) 
                count+=1
                cursor.execute(add_velocity, data_velocity)
    cnx.commit()
    print(cursor.rowcount, "record inserted.") 
    
# =============================================================================
# In order to keep your files separate and make sure there is no data dupes, 
# get rid of the processed data.  
# =============================================================================
def movefile(filename, desitnation_filename):
    os.rename(filename, desitnation_filename)    

# =============================================================================
# This carries out the insertion of all data columns. There is a counter to access
# timeStep. 
# =============================================================================
def insertAll(file_name, file_counter, datadir, datadir_processed):
        insertB(cursor, file_counter, datadir, file_name)
        insertI(cursor, file_counter, datadir, file_name)
        #make countR counter to avoid putting in R and V values after bounds = false = 1
        countR = insertR(cursor, file_counter, datadir, file_name)
        insertV(cursor, file_counter, datadir, file_name, countR)
        #move the processed file to avoid data dupes
        movefile(os.path.join(datadir, file_name), os.path.join(datadir_processed, file_name))
        file_counter+=1
        return file_counter
           
def Main(cursor):
    datadir = '/Users/Tamboli/Documents/data/sample_trajectory_files/'
    input_files = [file for file in os.listdir(datadir) if os.path.isfile(os.path.join(datadir, file)) and (file.endswith('.h5') or file.endswith('hdf5'))]
    print ( str(input_files)[1:-1]) #print all names of HDF files
    datadir_processed = '/Users/Tamboli/Documents/data/processed/'
    if not os.path.exists(datadir_processed): #create processed data folder
        os.makedirs(datadir_processed)
    file_counter=1 #initialize counter
    while len(input_files) != 0:
        for file_name in input_files:
            file_counter = insertAll(file_name, file_counter, datadir, datadir_processed)
            input_files.remove(file_name)
            print(file_counter)


print (__name__)
if __name__ == "__main__":
   Main(cursor)
