import sys, os.path
from time import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prefs.Prefs import Prefs
from strom import StromquistKnives, StromquistP1Right, StromquistP1MidRight, StromquistAllRight, StromquistAllMidRight

if __name__ == '__main__':
  pass

p1 = Prefs.fromFile("../../data/ascending")
p2 = Prefs.fromFile("../../data/descending")
p3 = Prefs.fromFile("../../data/uniform")

def runOneTest(name,p1,p2,p3, type, resolution=0.001):
    dc = type(p1, p2, p3, False, resolution)
    result = dc.run()
    pi1, pi2, pi3 = result
    received_vals = [piece['winnerValue'] for piece in result]
    envy =  checkForEnvy(result, resolution)
    return received_vals, envy


def checkForEnvy(pieces, resolution):
  received_vals = [piece['winnerValue'] for piece in pieces]
  total_envy = [0, 0, 0]

  for pnum in range(3):
    piece = pieces[pnum]
    piece_envy = [0, 0, 0]
    for k in range(3):
      otherval = piece['values'][k]
      if otherval != piece['winnerValue'] and otherval > received_vals[k]:
        diff = otherval - received_vals[k]
        if diff > resolution*1.1:
          piece_envy[k] += diff

    total_envy = [a + b for a,b in zip(piece_envy, total_envy)]

  return total_envy


def piecewiseAdd(l1, l2):
  return [a + b for a,b in zip(l1, l2)]

def runStrom(typeOfStrom, numRuns, rand_prefs):
  total_vals = [0, 0, 0]
  total_envy = [0, 0, 0]

  for i in range(numRuns):
    p1, p2, p3 = rand_prefs[i]
    vals, envy = runOneTest(str(i), p1, p2, p3, typeOfStrom)
    total_vals = piecewiseAdd(total_vals, vals)
    total_envy = piecewiseAdd(total_envy, envy)

  avg_vals = [val/numRuns for val in total_vals]
  print "Envy: " + str(envy)
  print "Avg. vals: " + str(avg_vals)
  print "Total value: " + str(sum(avg_vals))
  print


numRuns = int(sys.argv[1])
randp = int(sys.argv[2])

print "Running %s times per strategy" % sys.argv[1]
print "Random Preferences with %s avg intervals" % sys.argv[2]
print

rand_prefs = []
for i in range(numRuns):
  rand_prefs.append((Prefs.random(randp), Prefs.random(randp), Prefs.random(randp)))
print "Regular Stromquist:"
runStrom(StromquistKnives, numRuns, rand_prefs)
print "P1 Right"
runStrom(StromquistP1Right, numRuns, rand_prefs)
print "P1 Mid Right"
runStrom(StromquistP1MidRight, numRuns, rand_prefs)
print "All Right"
runStrom(StromquistAllRight, numRuns, rand_prefs)
print "All Mid Right"
runStrom(StromquistAllMidRight, numRuns, rand_prefs)

