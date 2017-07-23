import requests


class Weather(object):

    def __init__(self, endpoint, key):
        self.endpoint = endpoint
        self.key = key

    def daily_forecast(self, city):
        r = requests.get(self.endpoint+"/forecast/daily?appid="+self.key+"&units=metric&id="+city+"&cnt=1")
        return r.json()

    def current(self, city):
        r = requests.get(self.endpoint+"/weather?appid="+self.key+"&id="+city)
        return r.json()
