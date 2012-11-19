import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prefs.Prefs import Prefs
from strom import StromquistKnives

if __name__ == '__main__':
  pass

p1 = Prefs.fromFile("../../data/ascending")


stromK = StromquistKnives(p1, p1, p1)

print "Halfway value: ", stromK.findHalfWayPoint(p1, 0, 1)




