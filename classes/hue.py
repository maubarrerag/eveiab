import requests


class Huebridge(object):

    def __init__(self, bridge, device, username):
        self.bridge = bridge
        self.device = device
        self.username = username

    def getlights(self):
        res = requests.get(self.bridge+"/"+self.username+"/lights", verify=False, timeout=10)
        return res.json()

    def turnon(self, light):
        res = requests.put(self.bridge+"/"+self.username+"/lights/"+light+"/state", json={"on": True}, verify=False, timeout=10)
        return res.json()

    def turnoff(self, light):
        res = requests.put(self.bridge+"/"+self.username+"/lights/"+light+"/state", json={"on": False}, verify=False, timeout=10)
        return res.json()
