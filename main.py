import configparser
import time
import datetime
from classes.db import Sqlite
from classes.weather import Weather
from classes.hue import Huebridge


def weatherupdate(config):
    wea = Weather(config.get("weather", "endpoint"), config.get("weather", "key"))
    res = wea.current(config.get("weather", "city"))
    sql = Sqlite()
    sql.connect(config.get("global", "database"))
    sql.execute("insert into weather_info values(1,?,DATETIME('now'))", (res, ))
    sql.commit()


def todayAt(hr, min=0):
    now = datetime.datetime.now()
    return now.replace(hour=hr, minute=min)


def getweatherinfo(config):
    sql = Sqlite()
    sql.connect(config.get("global", "database"))


def checktime(config):
    weathertime = config.get("weather", "update").split(":")
    updateTime = todayAt(int(weathertime[0]), int(weathertime[1]))
    now = datetime.datetime.now()
    if updateTime.hour == now.hour and updateTime.minute == now.minute:
        weatherupdate(config)
    else:
        #Check if we need to turn on/off the lights
        getweatherinfo(config)


def createcron(config):
    while(True):
        checktime(config)
        time.sleep(60)


def main():
    print("Start main job")
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('eveiab.conf')
    createcron(config)


if __name__ == '__main__':
    main()
