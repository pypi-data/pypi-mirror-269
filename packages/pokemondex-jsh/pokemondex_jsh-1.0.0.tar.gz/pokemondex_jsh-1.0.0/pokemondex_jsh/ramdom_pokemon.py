import pandas as pd
import pkg_resources

class RamdomPokemon:
      FILE_PATH = pkg_resources.resource_filename(__name__, "pokemon.csv")
      def __init__(self):
          self._file = pd.read_csv(self.FILE_PATH)
          self._pokemon =None
          self._number = None
          self._name = None
          self._type1 = None
          self._type2 = None
          self._total = None
          self._hp = None
          self._attack = None
          self._defense = None
          self._spatk = None
          self._spdef = None
          self._speed = None
          self._generation = None
          self._legendary = None

      def generate_random(self):
         self._pokemon =self._file.sample()
         self._number = self._pokemon["#"].values[0]
         self._name = self._pokemon["Name"].values[0]
         self._type1 = self._pokemon["Type 1"].values[0]
         self._type2 = self._pokemon["Type 2"].values[0]
         self._total = self._pokemon["Total"].values[0]
         self._hp = self._pokemon["HP"].values[0]
         self._attack = self._pokemon["Attack"].values[0]
         self._defense = self._pokemon["Defense"].values[0]
         self._spatk = self._pokemon["Sp. Atk"].values[0]
         self._spdef = self._pokemon["Sp. Def"].values[0]
         self._speed = self._pokemon["Speed"].values[0]
         self._generation = self._pokemon["Generation"].values[0]
         self._legendary = self._pokemon["Legendary"].values[0]

      def getpokemon(self):
          return self._pokemon

      def getnumber(self):
          return self._number

      def getname(self):
          return self._name

      def gettype1(self):
          return self._type1

      def gettype2(self):
          return self._type2

      def gettotal(self):
          return self._total

      def gethp(self):
          return self._hp

      def getattack(self):
          return self._attack

      def getdefense(self):
          return self._defense

      def getspatk(self):
          return self._spatk

      def getspdef(self):
          return self._spdef

      def getspeed(self):
          return self._speed

      def getgeneration(self):
          return self._generation

      def getlegendary(self):
          return self._legendary

