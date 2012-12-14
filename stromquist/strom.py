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
   
    pYknife, pYplayer, pZplayer = (None, None, None)


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

    print "Final Values:"
    print "Player {3} From {0} to {1}, value: {2}".format(0, ref_knife_pos, pXval, cuttingIndex)
    print "Player {3} From {0} to {1}, value: {2}".format(ref_knife_pos, pYknife, pYval, pYplayer)
    print "Player {3} From {0} to {1}, value: {2}".format(pYknife, 1, pZval, pZplayer)

    pieces = [None, None, None]
    pieces[cuttingIndex] = pieceX
    pieces[pYplayer] = pieceY
    pieces[pZplayer] = pieceZ

    print pieces

    endPoints = [0, 0, 0]
    endPoints[cuttingIndex] = [0, ref_knife_pos]
    endPoints[pYplayer] = [ref_knife_pos, pYknife]
    endPoints[pZplayer] = [pYknife, 1]

    return records, pieces, endPoints

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


def isCloseEnough(v1, v2, tolerance=0.001):
  return abs(v1 - v2) <= tolerance
