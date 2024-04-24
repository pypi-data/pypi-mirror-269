import pandas as pd
import pkg_resources

class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, "pokemon.csv") #archivo ="pokemon.csv"

    # Se inicializan las variables
    def _init_(self):
        self._file = pd.read_csv(self.FILE_PATH)
        self._pokemon = None
        self._number = None
        self._name = None
        self._type1 = None
        self._type2 = None
        self._total = None
        self._HP = None
        self._attack = None
        self._Defense = None
        self._SpAtk = None
        self._SpDef = None
        self._speed = None
        self._generation = None
        self._legendary = None

    # Rol de seters
    def generate_random(self):
        self._pokemon = self._file.sample()
        self._number = self._pokemon["#"].values[0]
        self._name = self._pokemon["Name"].values[0]
        self._type1 = self._pokemon["Type 1"].values[0]
        self._type2 = self._pokemon["Type 2"].values[0]
        self._total = self._pokemon["Total"].values[0]
        self._HP = self._pokemon["HP"].values[0]
        self._attack = self._pokemon["Attack"].values[0]
        self._Defense = self._pokemon["Defense"].values[0]
        self._SpAtk = self._pokemon["Sp. Atk"].values[0]
        self._SpDef = self._pokemon["Sp. Def"].values[0]
        self._speed = self._pokemon["Speed"].values[0]
        self._generation = self._pokemon["Generation"].values[0]
        self._legendary = self._pokemon["Legendary"].values[0]

    # Rol de geters
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
        return self._HP

    def getAttack(self):
        return self._attack

    def getDefense(self):
        return self._Defense

    def getSpAtk(self):
        return self._SpAtk

    def getSpDef(self):
        return self._SpDef

    def getSpeed(self):
        return self._speed

    def getGeneration(self):
        return self._generation

    def getLegendary(self):
        return self._legendary


#Probando la clase
#pokemon=RandomPokemon()
#pokemon.generate_random ()
#print(pokemon.getPokemon())



