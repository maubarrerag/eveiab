import json
import configparser
import os


def main():
    print "Start main job"
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('eveiab.conf')

if __name__ == '__main__':
    main()
