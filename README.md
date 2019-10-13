# HDF_to_SQL
converts HDF files to MySQL

This code takes a hierarchical data file and changes each level into a table that works with SQL.
This was helpful in my lab where we are trying to make data collection and analysis easier with SQL. 
The change from HDF to database was prompted by the massive amount of data, but more importantly there were too many issues and inconveniences with accessing data and creating SQL-like relationships between datasets. 

With this, it is possible to take bools and ints from HDF and put them into MySQL. 
It uses a Python script to do SQL commands and create new schemas in MySQL. 
