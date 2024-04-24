import pandas as pd
import pkg_resources

class RandomPokemon:
 FILE_PATH = pkg_resources.resource_filename(__name__,"pokemon.csv")

 def __init__(self):
     self._file = pd.read_csv(self.FILE_PATH)
     self._number = None
     self._name = None
     self._type1 = None
     self._type2 = None
     self._total = None
     self._health = None
     self._attack = None
     self._defen = None
     self._spatk = None
     self._speed = None
     self._gennum = None
     self._legend = None

 def generate_random(self):
     self._pokemon = self._file.sample()
     self._number = self._pokemon["#"].values[0]
     self._name = self._pokemon["Name"].values[0]
     self._type1 = self._pokemon["Type 1"].values[0]
     self._type2 = self._pokemon["Type 2"].values[0]
     self._total = self._pokemon["Total"].values[0]
     self._health = self._pokemon["HP"].values[0]
     self._attack = self._pokemon["Attack"].values[0]
     self._defen = self._pokemon["Defense"].values[0]
     self._spatk = self._pokemon["Sp. Atk"].values[0]
     self._spdef = self._pokemon["Sp. Def"].values[0]
     self._speed = self._pokemon["Speed"].values[0]
     self._numgen = self._pokemon["Generation"].values[0]
     self._legend = self._pokemon["Legendary"].values[0]

 def getPokemon(self):
     return self._pokemon

 def getNumber(self):
     return self._number

 def getName(self):
     return self._name

 def getType1(self):
     return self._type1

 def getType2(self):
     return self._type2

 def getTotal(self):
     return self._total

 def getHP(self):
     return self._health

 def getAtk(self):
     return self._attack

 def getDef(self):
     return self._defen

 def getSpAtk(self):
     return self._spatk

 def getSpDef(self):
     return self._spdef

 def getSpeed(self):
     return self._speed

 def getGenNum(self):
     return self._numgen

 def getLegend(self):
     return self._legend
