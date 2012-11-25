import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prefs.Prefs import Prefs
from strom import StromquistKnives

if __name__ == '__main__':
  pass


f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]

p1 = Prefs.fromFile("f1")
p2 = Prefs.fromFile("f2")
p3 = Prefs.fromFile("f3")


stromK = StromquistKnives(p1, p2, p3)
