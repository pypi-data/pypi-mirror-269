import pandas as pd
import pkg_resources

class RandomPokemon:
      FILE_PATH = pkg_resources.resource_filename(__name__, 'Poc.csv')
      def __init__(self):
            self.file = pd.read_csv(self.FILE_PATH)
            self._pokemon = None
            self._number = None
            self._Name = None
            self._Type1 = None
      def generate_pokemon(self):
            self._pokemon = self.file.sample()
            self._number = self._pokemon["#"].values[0]
            self._name = self._pokemon["Name"].values[0]
            self._Type1 = self._pokemon["Type 1"].values[0]
            self._Type2 = self._pokemon["Type 2"].values[0]
            self._Total= self._pokemon["Total"].values[0]
            self._HP = self._pokemon["HP"].values[0]
            self._Attack = self._pokemon["Attack"].values[0]
            self._Defense = self._pokemon["Defense"].values[0]
            self._Sp_Atk = self._pokemon["Sp. Atk"].values[0]
            self._Sp_Def = self._pokemon["Sp. Def"].values[0]
            self._Speed = self._pokemon["Speed"].values[0]
            self._Legendary = self._pokemon["Legendary"].values[0]
            self._Generation = self._pokemon["Generation"].values[0]

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
      def get_HP(self):
            return self._HP
      def get_Attack(self):
            return self._Attack
      def get_Defense(self):
            return self._Defense
      def get_Sp_Atk(self):
            return self._Sp_Atk
      def get_Sp_Def(self):
            return self._Sp_Def
      def get_Speed(self):
            return self._Speed
      def get_Legendary(self):
            return self._Legendary
      def get_Generation(self):
            return self._Generation







