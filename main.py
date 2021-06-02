from OCBA import OCBAState
from UCT import UCBState
import comparison

testPositions1 = [[0]*6, [0]*6, [0]*6, [0]*6, [0]*6, [0]*6, [0]*6]
testPositions2 = [[0]*6, [0]*6, [1,1,2,1,0,0], [2,2,1,0,0,0], [2,2,0,0,0,0], [1,1,0,0,0,0], [0]*6]
testPositions3 = [[1,0,0,0,0,0],[1,0,0,0,0,0],[2,0,0,0,0,0],[2,2,1,0,0,0],[2,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0]]
testPositions4 = [[1,2,2,2,1,0],[2,1,2,1,0,0],[1,0,0,0,0,0],[1,1,2,1,2,0],[0]*6,[2,2,2,1,0,0],[1,0,0,0,0,0]]

# the testPositions can be any of the 4
comparison.comparePlot(1, [10, 300], 10, 2, testPositions3)
# comparison.OCBAGame(1, [5, 50], 3)
# comparison.UCBGame(1, [5, 50], 2)
# comparison.playAgainst(1, [10, 50], 3, 2, 1)
# comparison.compareDepth(3, 20, 2, 2, testPositions2)
