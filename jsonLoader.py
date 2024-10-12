import json

class jsonL:
    def __init__(self):
        level = open("level1.json","r")
        self.level_dic = json.loads(level.read())

    def getPlatforms(self):
        return self.level_dic["platforms"]