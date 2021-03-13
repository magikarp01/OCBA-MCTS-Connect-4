import random
import array
from array import *

class node:
    def __init__(self, positions = [[0] * 6 for _ in range(7)], budget = 0, initSamplingBudget = 0):
        self.positions = positions
        self.children = []
        self.totBudget = budget
        self.initSamplingBudget = initSamplingBudget

    #overall data
    positions = []
    totBudget = 0
    initSamplingBudget = 0 #n_0, initial number of explorations

    #contains data for each action
    actions = []
    budgetAlloc = {}
    qHats = {}#arrays of qhats for each action
    qBars = {}#qbars of each action
    sigmas = []
    deltas = []

    #
    vstar = -1
    optimalAction = -1
    numSamples = 0

    children = []


    def add_child(self, state):
        self.children.append(state)

    def stdev(self):
        self.sigmas = []

    def kronecker(self):
        self.delta = []

    # 0 for none, 1 for this player, 2 for opponent
    def getPositions(self):
        return self.positions

    def acps(self):
        return  # score

    def getChildren(self):
        return  # self.children


    def getSigma(self, action):
        # variance /= 1/(self.numSamples-1)
        # variance =
        self.sigmas[action] = 0

    def getBudget(self):  # budget for children nodes
        # if self.optimalAction == 0:
        #     startAction = 1
        # else:
        #     startAction = 0
        # for action in self.actions:
        #     if action == self.optimalAction:
        #         continue
        #     elif action == startAction:
        #         continue
        #     ratio =
        #
        self.budget = {}



    #check if any more moves can be made
    def checkHorizon(self, positions):
        for x in range(7):
            if self.validMove(positions, x):
                return False
        return True


    def winCheck(self, positions): #check if state is in win, loss, or tie condition
        #tie is only if at horizon and no wins
        #can check wins efficiently with kernels and convolve2, "Python connect 4 check win function" on Stack Overflow
        #for now, just manually check each

        #diagonal wins
        for x in range(4):
            for y in range(3):
                if positions[x][y] == 1 and positions[x+1][y+1] == 1 and positions[x+2][y+2] == 1 and positions[x+3][y+3] == 1:
                    return 1
                elif positions[6-x][y] == 1 and positions[5-x][y+1] == 1 and positions[4-x][y+2] == 1 and positions[3-x][y+3] == 1:
                    return 1
                elif positions[x][y] == 2 and positions[x + 1][y + 1] == 2 and positions[x + 2][y + 2] == 2 and \
                        positions[x + 3][y + 3] == 2:
                    return 0
                elif positions[6 - x][y] == 2 and positions[5 - x][y + 1] == 2 and positions[4 - x][y + 2] == 2 and \
                        positions[3 - x][y + 3] == 2:
                    return 0

        #horizontal wins
        for y in range(6):
            for x in range(4):
                if positions[x][y] == 1 and positions[x+1][y] == 1 and positions[x+2][y] == 1 and positions[x+3][y] == 1:
                    return 1
                elif positions[x][y] == 2 and positions[x+1][y] == 2 and positions[x+2][y] == 2 and positions[x+3][y] == 2:
                    return 0

        #vertical wins
        for x in range(7):
            for y in range(3):
                if positions[x][y] == 1 and positions[x][y+1] == 1 and positions[x][y+2] == 1 and positions[x][y+3] == 1:
                    return 1
                elif positions[x][y] == 2 and positions[x][y+1] == 2 and positions[x][y+2] == 2 and positions[x][y+3] == 2:
                    return 0

        if self.checkHorizon(positions):
            return 1/2

        else: #return -1 if not in win, loss, tie currently
            return -1


    #for now, no win heuristic implemented
    def winHeuristic(self, positions):
        return 1/2

    def validMove(self, positions, action):
        return positions[action][5] == 0

    # returns height of position as a result of an action
    def actionHeight(self, positions, action):
        for height in range(6):
            if positions[action][height] == 0:
                return height
        return -1

    # randomly makes move, returns new positions
    # PDF is uniform, for now no checking if a winning move can be made
    # assumes action is valid
    def sampleY(self, positionsClone, whichPlayer):
        positions = positionsClone
        possibleMoves = []
        for x in range(7):
            if positions[x][5] == 0:
                possibleMoves.append(x)
        randX = possibleMoves[random.randint(0, len(possibleMoves)-1)]
        # print(possibleMoves)
        # print(randX)
        # print(self.actionHeight(positions, randX))
        # print(positions)
        positions[randX][self.actionHeight(positions, randX)] = whichPlayer
        # print(positions)
        return positions


    def rollout(self, numMoves, whichPlayer):
        # get sample Q-hat by randomly simulating moves up to budget from parent
        #numMoves is total number of moves to make, max is 7*6 = 42
        #for now, every move is made uniformly random and we go to the end
        positions = self.getPositions()
        if self.winCheck(positions) != -1:
            return self.winCheck(positions)

        for move in range(numMoves):
            positions = self.sampleY(positions, whichPlayer)
            print(positions)
            if self.winCheck(positions) != -1:
                return self.winCheck(positions)

            if whichPlayer == 2:
                whichPlayer = 1
            elif whichPlayer == 1:
                whichPlayer = 2


        return self.winHeuristic(positions)



    def expand(self):
        # expand tree by getting possible moves from positions
        #A is choice of putting in each of 7 columns
        return

    def newPositions(self, move1, move2):
        self.positions[move1[0]][move1[1]] = 1
        self.positions[move2[0][move2[1]]] = 2
