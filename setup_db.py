#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys

import pymysql

from getpass import getpass

import configparser

config = configparser.ConfigParser()  # define config file
config.read("config.ini") #read config file

db_host = config.get('db', 'db_host').strip()
db_user = config.get('db', 'db_user').strip()
db_password = config.get('db', 'db_password').strip()
db_name = config.get('db', 'db_name').strip()

def mysqlconnect_install(root_password):
    # To connect MySQL database
    try:
        conn = pymysql.connect(host=db_host,
                               user='root',
                               password=root_password)
    except pymysql.Error as e:
        print("Could not connect %d: %s" % (e.args[0], e.args[1]))
    else:
        cur = conn.cursor()

    return conn, cur


def run_sql(cur, sql):

    try:
        cur.execute(sql)
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    # else:
    #    print("OK\nAffected rows = {}".format(cur.rowcount))

    result = (cur.fetchall())

    return result


def mysqlclose(conn):
    conn.commit()
    conn.close


def mariadb_setup():
    while True:
        root_password = getpass(
            "MySQL root password? (Exit with 'q', skip with 's') ")

        if root_password.lower() == 'q':
            sys.exit(0)
        elif root_password.lower() == 's':
            return

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

    sql = ("CREATE TABLE IF NOT EXISTS " +
           db_name + ".temperature(time DATETIME PRIMARY KEY, temp REAL)")
    run_sql(cur, sql)

    sql = ("CREATE TABLE IF NOT EXISTS " +
           db_name + ".forecast(time DATETIME PRIMARY KEY, temp REAL, rain REAL, wind REAL, gti_instant REAL)")
    run_sql(cur, sql)
    
    sql = ("CREATE TABLE IF NOT EXISTS " +
           db_name + ".sun(day DATE PRIMARY KEY, sunrise DATETIME, sunset DATETIME)")
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


if __name__ == "__main__":
    mariadb_setup()
