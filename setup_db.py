#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys

from getpass import getpass

from sql import mysqlconnect_install, run_sql, mysqlclose

from readConfig import db_host, db_name, db_user, db_password
       
def setup_db():
    while True:
        root_password = getpass("MySQL root password? (Exit with 'q') ")
        
        if root_password.lower() == 'q':
            sys.exit(0)
            
        try:
            conn, cur = mysqlconnect_install(root_password)
        except:
            print("\nTry again")
        else:
            break
    
    sql = "select @@version"
    output = run_sql(cur, sql) 
    print(f'\nConnected to db {output[0][0]}')
    
    print(f'\nCreating database \'{db_name}\'...')
    sql = "CREATE DATABASE IF NOT EXISTS " + db_name
    run_sql(cur, sql)
    
    print(f'\nCreating tables...')
    sql = ("CREATE TABLE IF NOT EXISTS " + 
           db_name + ".price(hour DATETIME PRIMARY KEY, SEK_per_kWh REAL)")
    run_sql(cur, sql)
    
    print(f'\nCreating user...')
    sql = ("CREATE USER IF NOT EXISTS " + 
           db_user + "@" + 
           db_host + " IDENTIFIED BY '" + 
           db_password + "'")
    run_sql(cur, sql)
    
    print(f'\nGrant privileges...')
    sql = ("GRANT ALL PRIVILEGES ON " + 
           db_name + ".* TO " + 
           db_user + "@" + 
           db_host)
    print(sql)
    run_sql(cur, sql)
    
    print(f'\nFlush privileges...')
    sql = ("FLUSH PRIVILEGES")
    run_sql(cur, sql)
    
    print(f'\nClose db connection...')
    mysqlclose(conn)
    
if __name__ == "__main__" : 
    setup_db()
    