import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prefs.Prefs import Prefs
from strom import StromquistKnives

if __name__ == '__main__':
  pass

p1 = Prefs.fromFile("../../data/ascending")
p2 = Prefs.fromFile("../../data/descending")
p3 = Prefs.fromFile("../../data/uniform")


stromK = StromquistKnives(p1, p2, p3)





