import pandas as pd
import pkg_resources

class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, "pokemon.csv") #archivo ="pokemon.csv"

    def _init_(self):#De si mismo. Es decir que self hace referencia a la misma
        #Guion bajo_ enfrente de la variable para uso de variables privadas
        self._file=pd.read_csv(self.FILE_PATH)
        self._pokemon=None
        self._number=None
        self._name=None
        self._type1=None
        self._type2=None


    def generate_random (self):
        self._pokemon=self._file.sample()
        #Inicializa el numero
        self._number=self._pokemon["#"].values[0]
        self._name=self._pokemon["Name"].values[0]
        self._type1=self._pokemon["Type 1"].values[0]
        self._type2=self._pokemon["Type 2"].values[0]
        self.total=self._pokemon["Total"].values[0]
        self._HP=self._pokemon["HP"].values[0]
        self.attack=self._pokemon["Attack"].values[0]
        self.defense=self._pokemon["Defense"].values[0]
        self._sp=self._pokemon["Sp. Def"].values[0]
        self._speed=self._pokemon["Speed"].values[0]
        self.generation=self._pokemon["Generation"].values[0]
        self._legendary=self._pokemon["Legendary"].values[0]


    def getPokemon (self):
        return self._pokemon
    def getNumber (self):
        return self._number
    def getName (self):
        return self._name
    def getType1 (self):
        return self._type1
    def getType2 (self):
        return self._type2
    def getTotal (self):
        return self.total
    def getHP (self):
        return self._HP
    def getAttack (self):
        return self._attack
    def getDefense (self):
        return self._defense
    def getSp (self):
        return self._sp
    def getSpeed (self):
        return self._speed
    def getGeneration (self):
        return self._generation
    def getLegendary (self):
        return self._legendary



