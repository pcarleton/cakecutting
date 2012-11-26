class StromquistKnives(object):

  def __init__(self, p1, p2, p3, resolution=0.001):
    self.p1 = p1
    self.p2 = p2
    self.p3 = p3
    self.resolution = resolution

  def run(self):

    prefs = (self.p1, self.p2, self.p3)
    resolution = self.resolution
    
    ref_knife_pos = resolution
    p_knives = [0, 0, 0]

    records = []

    cuttingIndex = -1
    while cuttingIndex < 0:
      records.append(list(p_knives))
      #Update knife positions
      for i in range(3):
        p_knives[i] = self.findHalfWayPoint(prefs[i], ref_knife_pos, 1)

      #Determine if a cut should be made
      for i in range(3):
        pieceX = prefs[i].valueOfPiece(0, ref_knife_pos)
        pieceY = prefs[i].valueOfPiece(ref_knife_pos, p_knives[1])
        pieceZ = prefs[i].valueOfPiece(p_knives[1], 1)

        if pieceX >= (1/3.0) and pieceX > pieceY and pieceX > pieceZ:
          cuttingIndex = i
          break

      ref_knife_pos += resolution


    # Get a list of the players who didn't cut
    remainingPlayers = range(3)
    remainingPlayers.remove(cuttingIndex)

    leftPlayer = remainingPlayers[0]
    rightPlayer = remainingPlayers[1]
   
   
    pYknife, pYplayer, pZplayer = (None, None, None)
    #Pick which other knife cuts
    if p_knives[leftPlayer] < p_knives[rightPlayer]:
      pYknife = p_knives[leftPlayer]
      pYplayer = leftPlayer
      pZplayer = rightPlayer
    else:
      pYknife = p_knives[rightPlayer]
      pYplayer = rightPlayer
      pZplayer = leftPlayer
      
    pXval = prefs[cuttingIndex].valueOfPiece(0, ref_knife_pos)
    pYval = prefs[pYplayer].valueOfPiece(ref_knife_pos, pYknife)
    pZval = prefs[pZplayer].valueOfPiece(pYknife, 1)


    print "Final Values:"
    print "Player {3} From {0} to {1}, value: {2}".format(0, ref_knife_pos, pXval, cuttingIndex)
    print "Player {3} From {0} to {1}, value: {2}".format(ref_knife_pos, pYknife, pYval, pYplayer)
    print "Player {3} From {0} to {1}, value: {2}".format(pYknife, 1, pZval, pZplayer)

    return records, (pXval, pYval, pZval)
        
  def findHalfWayPoint(self, prefs, left, right):
    total_val =  prefs.valueOfPiece(left, right)
    half_val = total_val / 2.0

    sl = left
    sr = right
    mid = (sr + sl) / 2.0
    for i in range(100):
      mid = (sr + sl) / 2.0
      piece_val = prefs.valueOfPiece(left, mid)
      if isCloseEnough(piece_val, half_val):
        return mid
      else:
        if piece_val > half_val:
          sr = mid
        else:
          sl = mid
    return mid


def isCloseEnough(v1, v2, tolerance=0.01):
  return abs(v1 - v2) <= tolerance
