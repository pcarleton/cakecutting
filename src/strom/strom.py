from prefs.Prefs import Prefs
from time import time

class StromquistKnives(object):

  def __init__(self, p1, p2, p3, verbose=1, resolution=0.001):
    self.p1 = p1
    self.p2 = p2
    self.p3 = p3
    self.verbose = verbose
    self.resolution = resolution


  def run(self):
    self.halfwayTime = 0
    t0 = time()
    prefs = (self.p1, self.p2, self.p3) 
    resolution = self.resolution
    ref_knife_pos = resolution
    p_knives = [0, 0, 0]


    cuttingIndex = -1
    while cuttingIndex < 0:
      #Update knife positions
      p_knives = self.updateKnives(prefs, ref_knife_pos)

      secondCuttingKnife = sorted(list(p_knives))[1]

      #Determine if a cut should be made
      for i in range(3):
        pieceX = prefs[i].valueOfPiece(0, ref_knife_pos)
        pieceY = prefs[i].valueOfPiece(ref_knife_pos, secondCuttingKnife)
        pieceZ = prefs[i].valueOfPiece(secondCuttingKnife, 1)

        if pieceX >= (1/3.0) and pieceX > pieceY and pieceX > pieceZ:
          cuttingIndex = i
          break

      ref_knife_pos += resolution


    # Get a list of the players who didn't cut
    remainingPlayers = range(3)
    remainingPlayers.remove(cuttingIndex)

    leftPlayer = remainingPlayers[0]
    rightPlayer = remainingPlayers[1]
   
    pYplayer, pZplayer = (None, None)

    pYknife = sorted(list(p_knives))[1]

    #Pick which other knife cuts
    if p_knives[leftPlayer] < p_knives[rightPlayer]:
      pYplayer = leftPlayer
      pZplayer = rightPlayer
    else:
      pYplayer = rightPlayer
      pZplayer = leftPlayer


    pieceX = self.createPiece(0, ref_knife_pos, cuttingIndex)
    pieceY = self.createPiece(ref_knife_pos, pYknife, pYplayer)
    pieceZ = self.createPiece(pYknife, 1, pZplayer)
      
    pXval = prefs[cuttingIndex].valueOfPiece(0, ref_knife_pos)
    pYval = prefs[pYplayer].valueOfPiece(ref_knife_pos, pYknife)
    pZval = prefs[pZplayer].valueOfPiece(pYknife, 1)

    pieces = [None, None, None]
    pieces[cuttingIndex] = pieceX
    pieces[pYplayer] = pieceY
    pieces[pZplayer] = pieceZ

    if self.verbose:
      print "Final Values:"
      print "Player {3} From {0} to {1}, value: {2}".format(0, ref_knife_pos, pXval, cuttingIndex)
      print "Player {3} From {0} to {1}, value: {2}".format(ref_knife_pos, pYknife, pYval, pYplayer)
      print "Player {3} From {0} to {1}, value: {2}".format(pYknife, 1, pZval, pZplayer)
      print "Run time: " + str(time() - t0)

      print "Time in  halfway: " + str(self.halfwayTime)
    return pieces 


  def createPiece(self, left, right, winner):
    prefs = (self.p1, self.p2, self.p3)
    piece = {}
    piece['left'] = left
    piece['right'] = right
    values = [prefs[i].valueOfPiece(left, right) for i in range(3)]
    piece['values'] = values
    piece['winner'] = winner
    piece['winnerValue'] = values[winner]

    return piece

  def updateKnives(self, prefs, ref_knife):
    new_p_knives = [0, 0, 0]
    for i in range(3):
      new_p_knives[i] = self.findHalfWayPoint(prefs[i], ref_knife, 1)

    return new_p_knives
    
        
  def findHalfWayPoint(self, prefs, left, right):
    t0 = time()
    total_val =  prefs.valueOfPiece(left, right)
    half_val = total_val / 2.0

    sl = left
    sr = right
    mid = (sr + sl) / 2.0
    for i in range(100):
      mid = (sr + sl) / 2.0
      piece_val = prefs.valueOfPiece(left, mid)
      if isCloseEnough(piece_val, half_val, self.resolution):
        self.halfwayTime += time() - t0
        return mid
      else:
        if piece_val > half_val:
          sr = mid
        else:
          sl = mid
    self.halfwayTime += time() - t0
    return mid
          


class StromquistP1Right(StromquistKnives):
  
  def updateKnives(self, prefs, ref_knife):
    new_p_knives = StromquistKnives.updateKnives(self, prefs, ref_knife)
    p1_knife = new_p_knives[0]
    right_most = max(new_p_knives)
    if p1_knife != right_most:
      new_p_knives[0] = right_most - self.resolution
    return new_p_knives
    


class StromquistP1MidRight(StromquistKnives):
  
  def updateKnives(self, prefs, ref_knife):
    new_p_knives = StromquistKnives.updateKnives(self, prefs, ref_knife)
    p1_knife = new_p_knives[0]
    right_most = max(new_p_knives)
    left_most = min(new_p_knives)
    if p1_knife != right_most and p1_knife != left_most:
      new_p_knives[0] = right_most - self.resolution
    return new_p_knives
 

class StromquistAllRight(StromquistKnives):
  
  def updateKnives(self, prefs, ref_knife):
    new_p_knives = StromquistKnives.updateKnives(self, prefs, ref_knife)
    right_most = max(new_p_knives)
    left_most = min(new_p_knives)
    mid_knife_p = 0
    for i in range(3):
      if new_p_knives[i] != left_most and new_p_knives != right_most:
        mid_knife_p = 0

    new_p_knives[mid_knife_p] = right_most - self.resolution
    return [right_most, right_most, right_most]
 
    

class StromquistAllMidRight(StromquistKnives):
  
  def updateKnives(self, prefs, ref_knife):
    new_p_knives = StromquistKnives.updateKnives(self, prefs, ref_knife)
    right_most = max(new_p_knives)
    left_most = min(new_p_knives)
    mid_knife_p = 0
    for i in range(3):
      if new_p_knives[i] != left_most and new_p_knives != right_most:
        mid_knife_p = 0

    new_p_knives[mid_knife_p] = right_most - self.resolution
    return new_p_knives

def isCloseEnough(v1, v2, tolerance=0.001):
  return abs(v1 - v2) <= tolerance
