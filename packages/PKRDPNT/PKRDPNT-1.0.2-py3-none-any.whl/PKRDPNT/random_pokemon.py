import pandas as pd
import pkg_resources


class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, 'pokemon.csv')

    def __init__(self):
        self.file = pd.read_csv(self.FILE_PATH)
        self._pokemon = None
        self._number = None
        self._name = None
        self._Type1 = None
        self._Type2 = None
        self._Total = None
        self._hp = None
        self._attack = None
        self._defense = None
        self._atsp = None
        self._dfsp = None
        self._sp = None
        self._generacion = None
        self._legend = None

    def generate_pokemon(self):
        self._pokemon = self.file.sample()
        self._number = self._pokemon["#"].values[0]
        self._name = self._pokemon["Name"].values[0]
        self._Type1 = self._pokemon["Type 1"].values[0]
        self._Type2 = self._pokemon["Type 2"].values[0]
        self._Total = self._pokemon["Total"].values[0]
        self._hp = self._pokemon["HP"].values[0]
        self._attack = self._pokemon["Attack"].values[0]
        self._defense = self._pokemon["Defense"].values[0]
        self._atsp = self._pokemon["Sp. Atk"].values[0]
        self._dfsp = self._pokemon["Sp. Def"].values[0]
        self._sp = self._pokemon["Speed"].values[0]
        self._generacion = self._pokemon["Generation"].values[0]
        self._legend = self._pokemon["Legendary"].values[0]

    def get_pokemon(self):
        return self._pokemon

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_Type1(self):
        return self._Type1

    def get_Type2(self):
        return self._Type2

    def get_Total(self):
        return self._Total

    def get_hp(self):
        return self._hp

    def get_attack(self):
        return self._attack

    def get_defense(self):
        return self._defense

    def get_atsp(self):
        return self._atsp

    def get_dfsp(self):
        return self._dfsp

    def get_sp(self):
        return self._sp

    def get_generacion(self):
        return self._generacion

    def get_legend(self):
        return self._legend