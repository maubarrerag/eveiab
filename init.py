#!/usr/bin/python
import configparser
import pprint
from classes import Sqlite

def createdb(name):
    sql = Sqlite()
    sql.connect(name)

def main():
    print("Initializing parameters for EveIAb")
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('eveiab.conf')
    print("Creating database")
    createdb(config.get("global", "database"))

if __name__ == '__main__':
    main()
