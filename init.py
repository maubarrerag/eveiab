#!/usr/bin/python
import configparser
from classes.db import Sqlite


def createdb(name):
    try:
        sql = Sqlite()
        sql.connect(name)
        sql.execute("create table weather_info(id int,json text)")
    except:
        print("Can\'t create database or tables")


def main():
    print("Initializing parameters for EveIAb")
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('eveiab.conf')
    print("Creating database")
    createdb(config.get("global", "database"))

if __name__ == '__main__':
    main()
