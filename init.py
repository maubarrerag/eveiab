#!/usr/bin/python
import configparser
import json
from classes.db import Sqlite
from classes.weather import Weather
from classes.hue import Huebridge


def createdb(name):
    try:
        sql = Sqlite()
        sql.connect(name)
        sql.execute("create table weather_info(id int,json text, update_t DATE)", ())
    except:
        print("Can\'t create database or tables")


def savefirst(name, info):
    try:
       sql = Sqlite()
       sql.connect(name)
       sql.execute("insert into weather_info values(1,?,DATETIME('now'))", (info, ))
       sql.commit()
    except:
        print("Problem saving information")
        raise


def weather(config):
    try:
        wea = Weather(config.get("weather", "endpoint"), config.get("weather", "key"))
        res = wea.current(config.get("weather", "city"))
        print("Getting information for city:"+res["name"])
        savefirst(config.get("global", "database"), json.dumps(res))
    except:
        print("Can\'t get weather information check weather params and service")
        raise


def hue(config):
    try:
        hu = Huebridge(config.get("hue", "bridge"), config.get("hue", "device"), config.get("hue", "username"))
        hu.getlights()
    except:
        print("Unable to connect to HUE Bridge")
        raise


def main():
    print("Initializing parameters for EveIAb")
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('eveiab.conf')
    print("Creating database")
    createdb(config.get("global", "database"))
    print("Testing weather service")
    weather(config)
    print("Testing HUE phillips service")
    hue(config)

if __name__ == '__main__':
    main()
