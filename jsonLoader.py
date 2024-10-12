import json


def getlvldata():
    platforms = open("level1.json","r")

    platformDictionaryEncoded = json.loads(platforms.read())

    print(platformDictionaryEncoded["platforms"])