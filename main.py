import configparser
import time
import datetime
import json
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


def lightswitch(state, config, lights):
    light_a = lights.split(",")
    hu = Huebridge(config.get("hue", "bridge"), config.get("hue", "device"), config.get("hue", "username"))
    for light in light_a:
        if state:
            hu.turnon(light)
        else:
            hu.turnoff(light)


def getweatherinfo(config, now):
    sql = Sqlite()
    sql.connect(config.get("global", "database"))
    cursor = sql.execute("select json from weather_info order by update_t desc limit 1", ())
    obj = json.loads(sql.fecth_one(cursor)[0])
    sunset = datetime.datetime.fromtimestamp(int(obj["sys"]["sunset"]))
    sunrise = datetime.daetime.fromtimestamp(int(obj["sys"]["sunrise"]))
    if sunset.hour == now.hour and sunset.minute == now.minute:
        lights = config.get("hue", "ligths_sunset")
        lightswitch(False, config, lights)
    if sunrise.hour == now.hour and sunrise.minute == now.minute:
        lights = config.get("hue", "ligths_sunrise")
        lightswitch(True, config, lights)


def checktime(config):
    weathertime = config.get("weather", "update").split(":")
    updateTime = todayAt(int(weathertime[0]), int(weathertime[1]))
    now = datetime.datetime.now()
    if updateTime.hour == now.hour and updateTime.minute == now.minute:
        weatherupdate(config)
    else:
        #Check if we need to turn on/off the lights
        getweatherinfo(config, now)


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
