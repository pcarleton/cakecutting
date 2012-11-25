from prefs.Prefs import Prefs

class StromquistKnives(object):

  def __init__(self, p1, p2, p3, resolution=0.01):
    self.p1 = p1
    self.p2 = p2
    self.p3 = p3

    #self.run((p1, p2, p3), resolution)


  def run(self, prefs, resolution):
    
    ref_knife_pos = resolution
    p_knives = [0, 0, 0]


  def findHalfWayPoint(self, prefs, left, right):
    total_val =  prefs.valueOfPiece(left, right)
    half_val = total_val / 2.0

    sl = left
    sr = right
    mid = (sr + sl) / 2.0
    for i in range(100):
      mid = (sr + sl) / 2.0
      print "Mid: ", mid
      piece_val = prefs.valueOfPiece(left, mid)
      print "Piece val: ", piece_val
      if isCloseEnough(piece_val, half_val):
        return mid
      else:
        if piece_val > half_val:
          sr = mid
        else:
          sl = mid
    print "none found"
    print "half val: ", half_val
    print "val found: ", prefs.valueOfPiece(left, mid)
    return mid
          




def isCloseEnough(v1, v2, tolerance=0.01):
  return abs(v1 - v2) <= tolerance
