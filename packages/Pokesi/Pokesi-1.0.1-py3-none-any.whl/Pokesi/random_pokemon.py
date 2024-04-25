import pandas as pd
import pkg_resources

class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, "pokemon.csv")

    def __init__(self):
        self._file = pd.read_csv(self.FILE_PATH)
        self._pokemon = None
        self._number = None
        self._name = None
        self._type1 = None

        def generate_random(self):
            self._pokemon = self.file.sample() #Generando un pokemon aleatorio
            self._number = self._pokemon["a"].values[0]
            self._name = self._pokemon["Name"].values[0]
            self._type1 = self._pokemon["Type1"].values[0]

        def get_pokemon(self):
            return self._pokemon

        def get_number(self):
            return self._number

        def getName(self):
            return self._name

        def getType1(self):
            return self._type1

        #Probando la clase
        pokemon = RandomPokemon()
        pokemon.generate_random()
        print(pokemon.getpokemon())
        print( pokemon.getName())


