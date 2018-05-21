import json
import bisect
import copy
import math

# Usage:
# somevar = importjson(filename)
# this will return a fullgame() object with all of the timetiles
# The filename should be formatted 'dummygame.json' if it's in the same directory
# To view the timetiles, use:
# printtiles(somevar)
# Timetiles are 8 minutes long, containing all units which were built during
# that duration

TIME_STEP=30.0
class timetile:
    playerdict = dict()

    # timeframe would be the index of the timetile
    # tiles are currently 8 minutes long, or TIME_STEP seconds
    def __init__(self, timeframe):
        self.tf = timeframe

class fullgame:
    p1t = []
    p2t = []

    def __init__(self, timelength):
        for i in range(0, timelength):
            self.p1t = self.p1t + [timetile(i)]
            self.p2t = self.p2t + [timetile(i)]

def importjson(filename):
    with open(filename) as f:
        idata = json.load(f)

    # set the dictionaries for each player
    p1 = idata["p1"]["units"]
    p2 = idata["p2"]["units"]

    # create a sequence of all the timestamps
    p1v = p1.values()
    p2v = p2.values()

    # find the max timestamp (the last unit created)
    vfull = p1v + p2v
    vals = []
    for i in vfull:
        vals = vals + i

    maxt = max(vals)

    # create the class objects
    # number of 8-minute time tiles in the game
    gametiles = int(math.ceil(maxt/TIME_STEP))
    fgame = fullgame(gametiles)

    # Iterate through the tile tiles for the game
    for i in range(0, gametiles):
        # The abridged dictionary for this time tile
        abrdict = dict()
        for k,v in p1.items():
            # Get the indices for the time cutoff of this tile
            tileindu = bisect.bisect_left(v,(i+1)*TIME_STEP)
            tileindl = bisect.bisect_left(v,(i)*TIME_STEP)

            # Abridge the dictionary to the tile
            abrdict[k] = v[tileindl:tileindu]

        # Set the abriged list for this tile
        fgame.p1t[i].playerdict = copy.deepcopy(abrdict)

        # Do the above for player 2
        for k,v in p2.items():
            tileindu = bisect.bisect_left(v,(i+1)*TIME_STEP)
            tileindl = bisect.bisect_left(v,(i)*TIME_STEP)
            abrdict[k] = v[tileindl:tileindu]
        fgame.p2t[i].playerdict = copy.deepcopy(abrdict)

    # Returns a fullgame object with p1t and p2t as lists of the timetiles
    # For instance, fgame.p1t[0] is the units for player 1 between 0 and TIME_STEPs
    return fgame

# Prints tiles and their times in a readable format
# fgame input is a fullgame() object
def printtiles(fgame):
    print("Player 1:")
    for i in fgame.p1t:
        print("Tile: " + str(i.tf) + ", t = " + str(i.tf*TIME_STEP) + " to " + str((i.tf+1)*TIME_STEP-1))
        print(i.playerdict)
    print("Player 2:")
    for i in fgame.p2t:
        print("Tile: " + str(i.tf) + ", t = " + str(i.tf*TIME_STEP) + " to " + str((i.tf+1)*TIME_STEP-1))
        print(i.playerdict)