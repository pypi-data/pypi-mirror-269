import pandas as pd
import pkg_resources


class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, "pokemon.csv")

    def __init_3222222222_(self):
        # _ variable privada
        self._file = pd.read_csv(self.FILE_PATH)
        self._pokemon = None
        # none=vacio
        self._number = None
        self._name = None
        self._type1 = None
        self._type2 = None
        self._total = None
        self._hp = None
        self._attack = None
        self._defense = None
        self._spAtk = None
        self._spDef = None
        self._speed = None
        self._generation = None
        self._legendary = None

    def generate_random(self):
        # sample genera una fila aleatoria
        self._pokemon = self._file.sample()
        self._number = self._pokemon["#"].values[0]
        self._name = self._pokemon["Name"].values[0]
        self._type1 = self._pokemon["Type 1"].values[0]
        self._type2 = self._pokemon["Type 2"].values[0]
        self._total = self._pokemon["Total"].values[0]
        self._hp = self._pokemon["HP"].values[0]
        self._attack = self._pokemon["Attack"].values[0]
        self._defense = self._pokemon["Defense"].values[0]
        self._spAtk = self._pokemon["Sp. Atk"].values[0]
        self._spDef = self._pokemon["Sp. Def"].values[0]
        self._speed = self._pokemon["Speed"].values[0]
        self._generation = self._pokemon["Generation"].values[0]
        self._legendary = self._pokemon["Legendary"].values[0]

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

    def getHp(self):
        return self._hp

    def getAtk(self):
        return self._attack

    def getDefense(self):
        return self._defense

    def getspAtk(self):
        return self._spAtk

    def getspDef(self):
        return self._spDef

    def getSpeed(self):
        return self._speed

    def getGeneration(self):
        return self._generation

    def getLegendary(self):
        return self._legendary

