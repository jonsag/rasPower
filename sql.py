#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import pymysql, sys

from readConfig import db_host, db_user, db_password, db_name, db_port

def mysqlconnect_install(root_password): 
    # To connect MySQL database 
    try:
        conn = pymysql.connect(host = db_host, 
                            user = 'root', 
                            password = root_password) 
    except pymysql.Error as e:
        print("Could not connect %d: %s" %(e.args[0], e.args[1]))
    else:
        cur = conn.cursor() 
    
    return conn, cur

def mysqlconnect(db_host, db_user, db_password, db_name, db_port): 
    # To connect MySQL database 
    try:
        conn = pymysql.connect(host = db_host, 
                               user = db_user, 
                               password = db_password, 
                               database = db_name, 
                               port = db_port)
         
    except pymysql.Error as e:
        print("Could not connect %d: %s" %(e.args[0], e.args[1]))
        sys.exit(0)
    else:
        cur = conn.cursor() 
    
    return conn, cur

def run_sql(cur, sql):
    
    try:
        cur.execute(sql)
    except pymysql.Error as e:
        print("Error %d: %s" %(e.args[0], e.args[1]))
        sys.exit(1)
    else:
        print("OK\nAffected rows = {}".format(cur.rowcount))
        
    output =(cur.fetchall())
    
    return output
    
def mysqlclose(conn):
    conn.commit()
    conn.close
    
def do_sql(sql):
    conn, cur = mysqlconnect(db_host, db_user, db_password, db_name, db_port)
    
    output = run_sql(cur, sql)
    
    mysqlclose(conn)
    
    return output
    
if __name__ == "__main__" : 
    conn, cur = mysqlconnect(db_host, db_user, db_password, db_name, db_port)
    
    sql = "select @@version"
    output = run_sql(cur, sql) 
    
    print(f'\nConnected to db {output[0][0]}')
    
    mysqlclose(conn)
