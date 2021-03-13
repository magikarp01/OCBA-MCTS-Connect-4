import random
import math
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
    budgetAlloc = [] #budget allocation for each child node
    qHats = [[], [], [], [], [], [], []] # arrays of qhats for each action
    qBars = [0]*7 # qbars of each action
    variances = [0]*7
    kroneckers = [0]*7
    numVisits = [0]*7 # for every visit to an action, there should be a qHat

    vstar = -1
    optimalActions = []
    numSamples = 0

    children = []

    # 0 for none, 1 for this player, 2 for opponent
    def getPositions(self):
        return self.positions

    def add_child(self, state):
        self.children.append(state)


    #it is possible
    def setOptimalActions(self):
        maxQBar = self.qBars[0]
        optimalActions = [0]
        for action in range(1, 7):
            if self.qBars[action] > maxQBar:
                optimalActions = [action]
                maxQBar = self.qBars[action]
            elif self.qBars[action] == maxQBar:
                optimalActions.append(action)
        self.optimalActions = optimalActions


    def updateVariance(self, action): #call whenever a new call to action has been done
        #instead of manually checking, we do a bit more efficient
        #update previous variance by
        prevVariance = self.variances[action]
        numVisits = self.numVisits[action]

        if numVisits > 1:
            newVariance = prevVariance * (numVisits-2)
            newVariance += (self.qHats[action][numVisits-1] - self.qBars[action])**2
            newVariance /= (numVisits-1)

        else:
            newVariance = 0

        # numVisits should never be 0 or 1, this function is only called when there has been a visit
        # and variance is only meaningful when there have been multiple samples

        self.variances[action] = newVariance


    def updateKronecker(self, action): #every use should be accompanied by a setOptimalActions()
        maxQBar = self.qBars[self.optimalActions[0]]
        self.kroneckers[action] = maxQBar - self.qBars[action]


    def updateBudget(self, totBudget):  # budget for children nodes, does not handle when an action cannot be made yet

        startAction = 0
        for action1 in range(7):
            if action1 not in self.optimalActions:
                startAction = action1
                break
        denom = self.variances[startAction]/(self.kroneckers[startAction]**2)


        ratios = [0]*7
        # numRatios = 0

        for action in range(7):
            if action in self.optimalActions:
                continue
            elif action == startAction:
                ratios[action] = 1
                # numRatios += 1
                continue
            else: # assumes kroneckers and variances != 0
                ratio = self.variances[startAction]/(self.kroneckers[startAction]**2)
                ratio /= denom
                ratios[action] = ratio
                # numRatios += 1


        #set up calculation for the proportion of the budget for optimal actions
        tempSum = 0 # sum of N^2/stdev
        for action in range(7):
            if ratios[action] != 0:
                tempSum += ratios[action]**2/self.variances[action] #stuff cancels
        tempSum = math.sqrt(tempSum)

        for action in self.optimalActions: #not sure if optimalProportion might be different for multiple optimal actions
            ratios[action] = math.sqrt(self.variances[action])*tempSum


        #calculate the actual budgets from the proportions
        total = 0
        budget = []
        for action in range(7):
            total += ratios[action]
        scale = (totBudget+1)/total # dunno how to handle fractions for now, prob ask Dr. Fu
        for action in range(7):
            budget[action] = scale*ratios[action]
        self.budgetAlloc = budget


    # def reward(self, action):


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
    def sampleNext(self, positions, whichPlayer):
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
            positions = self.sampleNext(positions, whichPlayer)
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
        positions = self.getPositions()
        positions[move1][self.actionHeight(positions, move1)] = 1
        positions[move2][self.actionHeight(positions, move2)] = 2
