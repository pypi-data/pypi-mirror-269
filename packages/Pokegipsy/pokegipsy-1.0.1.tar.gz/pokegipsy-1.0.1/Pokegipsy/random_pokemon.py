import pandas as pd
import pkg_resources


class RandomPokemon:
    # Ruta al archivo CSV de Pokémon usando pkg_resources
    FILE_PATH = pkg_resources.resource_filename(__name__, "pokemon.csv")

    # Constructor
    def __init__(self):
        self._file = pd.read_csv(self.FILE_PATH)  # se lee el archivo pandas
        self._number = None
        self._name = None
        self._type1 = None
        self._pokemon = None

    def generate_random(self):
        self._pokemon = self._file.sample()  # Con esta funcion se genera una columna aleatoria
        self._number = self._pokemon["#"].values[0]
        self._name = self._pokemon["Name"].values[0]
        self._type1 = self._pokemon["Type 1"].values[0]
        self._type2 = self._pokemon["Type 2"].values[0]
        self._total = self._pokemon["Total"].values[0]
        self._hp = self._pokemon["HP"].values[0]
        self._attack = self._pokemon["Attack"].values[0]
        self._defense = self._pokemon["Defense"].values[0]
        self._sp = self._pokemon["Sp. Atk"].values[0]
        self._sp1 = self._pokemon["Sp. Def"].values[0]
        self._speed = self._pokemon["Speed"].values[0]
        self._generation = self._pokemon["Generation"].values[0]
        self._legendary = self._pokemon["Legendary"].values[0]


     # get-mandar a llamar lo que esta en esa variable
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

    def getHP(self):
        return self._hp

    def getSpeed(self):
        return self._speed

    def getGeneration(self):
        return self._generation

    def getLegendary(self):
        return self._legendary

    def getDefense(self):
        return self._defense

    def getAttack(self):
        return self._attack

    def getSp(self):
        return self._sp

    def getSp1(self):
        return self._sp1



