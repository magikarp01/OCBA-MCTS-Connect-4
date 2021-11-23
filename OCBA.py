# todo: limit the total number of calculations
# todo: implement batch sampling

import random
import math
from array import *
from copy import deepcopy

# i may need to have getters and setters
class OCBAState:
    def __init__(self, positions=[[0] * 6 for _ in range(7)]):
        self.positions = positions
        self.children = []

        self.numVisits = 0

        self.actions = []
        self.budgetAlloc = []  # budget allocation for each child node
        self.qHats = [[], [], [], [], [], [], []]  # arrays of qhats for each action
        self.qBars = [0] * 7  # qbars of each action
        self.variances = [0] * 7
        self.kroneckers = [0] * 7
        self.numSamples = [0] * 7

        self.vHat = 0
        self.optimalActions = []

        self.children = []

        self.setActions()


    # overall data
    positions = []
    numVisits = 0
    initProbeBudget = 0  # n_0, initial number of explorations

    # contains data for each action
    actions = []
    budgetAlloc = []  # budget allocation for each child node
    qHats = [[], [], [], [], [], [], []]  # arrays of qhats for each action
    qBars = [0] * 7  # qbars of each action
    variances = [0] * 7
    kroneckers = [0] * 7
    numSamples = [0] * 7

    vHat = 0
    optimalActions = []

    children = []

    # 0 for none, 1 for this player, 2 for opponent
    def getPositions(self):
        return deepcopy(self.positions)

    def setActions(self):
        actions = []
        for x in range(7):
            if self.positions[x][5] == 0:
                actions.append(x)
        self.actions = actions

    def getOptimalAction(self):
        #print(self.optimalActions)
        if self.optimalActions[0] == 1:
            check = self.checkIfWinMove(self.positions, 1)
            if check != -1:
                return check
        return self.optimalActions[0]

    # run this at the very end
    def updateOptimalActions(self):
        self.setActions()
        maxQBar = self.qBars[0]
        optimalActions = [0]
        for action in self.actions:
            if self.qBars[action] > maxQBar:
                optimalActions = []
                optimalActions.append(action)
                maxQBar = self.qBars[action]
            elif self.qBars[action] == maxQBar:
                optimalActions.append(action)
        if maxQBar == 0: # cannot win
            optimalActions = self.actions # all of the moves are the same, loss
        self.optimalActions = optimalActions

    def updateVariance(self, action):  # call whenever a new call to action has been done
        # instead of manually checking, we do a bit more efficient
        # update previous variance by
        prevVariance = self.variances[action]
        numSamples = self.numSamples[action]

        if numSamples > 1:
            newVariance = prevVariance * (numSamples - 2)
            newVariance += (self.qHats[action][numSamples - 1] - self.qBars[action]) ** 2
            newVariance /= (numSamples - 1)

        else:
            newVariance = 0

        # numSamples should never be 0 or 1, this function is only called when there has been a visit
        # and variance is only meaningful when there have been multiple samples

        self.variances[action] = newVariance

    def updateKronecker(self, action):  # every use should be accompanied by a setOptimalActions()
        maxQBar = self.qBars[self.optimalActions[0]]
        self.kroneckers[action] = maxQBar - self.qBars[action]

    def updateBudget(self):

        startAction = -1
        for action in self.actions:
            if action not in self.optimalActions:
                if self.variances[action] != 0 and self.kroneckers[action] != 0:
                    startAction = action
                    break
        varFlag = True # if any of the nonoptimal moves have nonzero variance
        try:
            denom = self.variances[startAction] / (self.kroneckers[startAction] ** 2)
        except: # happens when all of the nonoptimal moves have zero variance
            varFlag = False
        ratios = [0] * 7

        for action in self.actions:
            if action in self.optimalActions:
                continue
            elif action == startAction:
                ratios[action] = 1
                continue
            else:  # assumes kroneckers and variances != 0
                ratio = self.variances[action] / (self.kroneckers[action] ** 2)
                try:
                    ratio /= denom
                except: # happens when all of the nonoptimal moves have zero variance, only one possible move
                    budget = [0] * 7
                    totBudget = 0
                    for action in self.actions:
                        totBudget += self.numSamples[action]
                    averageAlloc = (totBudget+1)/len(self.optimalActions)
                    for x in self.optimalActions:
                        budget[x] = averageAlloc

                    self.budgetAlloc = budget
                    return

                ratios[action] = ratio


        # set up calculation for the proportion of the budget for optimal actions
        tempSum = 0  # sum of N^2/stdev
        for action in self.actions:
            if ratios[action] != 0:
                tempSum += ratios[action] ** 2 / self.variances[action]  # stuff cancels
        tempSum = math.sqrt(tempSum)

        for action in self.optimalActions:  # not sure if optimalProportion might be different for multiple optimal actions
            ratios[action] = math.sqrt(self.variances[action]) * tempSum

        # calculate the actual budgets from the proportions
        total = 0
        budget = [0]*7
        totBudget = 0
        for action in self.actions:
            total += ratios[action]
            totBudget += self.numSamples[action]

        try:
            scale = (totBudget + 1) / total
            for action in range(7):
                budget[action] = scale * ratios[action]
        except:
            uniform = (totBudget+1)/7
            for action in range(7):
                budget[action] = uniform

        self.budgetAlloc = budget


    # check if any more moves can be made
    def checkHorizon(self, positions):
        for x in range(7):
            if positions[x][5] == 0:
                return False
        return True

    def winCheck(self, positions):  # check if state is in win, loss, or tie condition
        # tie is only if at horizon and no wins
        # can check wins efficiently with kernels and convolve2, "Python connect 4 check win function" on Stack Overflow
        # for now, just manually check each
        # alternatively, when performing action check
        # diagonal wins
        for x in range(4):
            for y in range(3):
                if positions[x][y] == 1 and positions[x + 1][y + 1] == 1 and positions[x + 2][y + 2] == 1 and \
                        positions[x + 3][y + 3] == 1:
                    return 1
                elif positions[6 - x][y] == 1 and positions[5 - x][y + 1] == 1 and positions[4 - x][y + 2] == 1 and \
                        positions[3 - x][y + 3] == 1:
                    return 1
                elif positions[x][y] == 2 and positions[x + 1][y + 1] == 2 and positions[x + 2][y + 2] == 2 and \
                        positions[x + 3][y + 3] == 2:
                    return 0
                elif positions[6 - x][y] == 2 and positions[5 - x][y + 1] == 2 and positions[4 - x][y + 2] == 2 and \
                        positions[3 - x][y + 3] == 2:
                    return 0

        # horizontal wins
        for y in range(6):
            for x in range(4):
                if positions[x][y] == 1 and positions[x + 1][y] == 1 and positions[x + 2][y] == 1 and positions[x + 3][
                    y] == 1:
                    return 1
                elif positions[x][y] == 2 and positions[x + 1][y] == 2 and positions[x + 2][y] == 2 and \
                        positions[x + 3][y] == 2:
                    return 0

        # vertical wins
        for x in range(7):
            for y in range(3):
                if positions[x][y] == 1 and positions[x][y + 1] == 1 and positions[x][y + 2] == 1 and positions[x][
                    y + 3] == 1:
                    return 1
                elif positions[x][y] == 2 and positions[x][y + 1] == 2 and positions[x][y + 2] == 2 and positions[x][
                    y + 3] == 2:
                    return 0

        if self.checkHorizon(positions):
            return 1 / 2

        else:  # return -1 if not in win, loss, tie currently
            return -1

    # for now, no win heuristic implemented
    def winHeuristic(self, positions):
        return 1 / 2

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

        randX = possibleMoves[random.randint(0, len(possibleMoves) - 1)]

        positions[randX][self.actionHeight(positions, randX)] = whichPlayer

        return positions


    def checkIfWinMove(self, positions, whichPlayer): #prob needs to be more efficient
        positions = deepcopy(positions)
        for action in range(7):
            if positions[action][5] == 0:
                actionHeight = self.actionHeight(positions, action)
                positions[action][actionHeight] = whichPlayer

                if whichPlayer == 1:
                    if self.winCheck(positions) == 1:
                        return action
                else:
                    if self.winCheck(positions) == 0:
                        return action
                positions[action][actionHeight] = 0

        return -1


    def rollout(self, numMoves, whichPlayer): #whichPlayer is 1 for self
        # get sample vHat
        positions = self.getPositions()
        winVal = self.winCheck(positions)
        if winVal != -1:
            return winVal

        for move in range(numMoves):
            prevPositions = deepcopy(positions)

            # want to make winning move and don't want to make losing move
            check1 = self.checkIfWinMove(prevPositions, 1)
            check2 = self.checkIfWinMove(prevPositions, 2)
            nextMoveFlag = True

            if whichPlayer == 1:
                if check1 != -1:
                    return 1
                elif check2 != -1:
                    nextMoveFlag = False
                    positions[check2][self.actionHeight(positions, check2)] = 1

            elif whichPlayer == 2:
                if check2 != -1:
                    return 0
                elif check1 != -1:
                    nextMoveFlag = False
                    positions[check1][self.actionHeight(positions, check1)] = 2

            if nextMoveFlag:
                positions = self.sampleNext(positions, whichPlayer)
            #print(positions)

            winVal2 = self.winCheck(positions)
            if winVal2 != -1:
                return winVal2

            if whichPlayer == 2:
                whichPlayer = 1
            elif whichPlayer == 1:
                whichPlayer = 2

        return self.winHeuristic(positions)


    def sampleY(self, action):
        positions = self.getPositions()
        positions[action][self.actionHeight(positions, action)] = 1

        check2 = self.checkIfWinMove(positions, 2) # if can make a winning move
        if check2 != -1:
            positions[check2][self.actionHeight(positions, check2)] = 2
            return positions

        check1 = self.checkIfWinMove(positions, 1)
        if check1 != -1: # if can block a losing move
            positions[check1][self.actionHeight(positions, check1)] = 2
            return positions

        positions = self.sampleNext(positions, 2)
        return positions

    def sampleReward(self):
        winCheck = self.winCheck(self.positions)
        if winCheck != -1:
            return winCheck
        else:
            return 0

    def sampleVHat(self, numRewardSamples):
        average = 0
        for x in range(numRewardSamples):
            average += self.rollout(42, 1)
        average /= numRewardSamples
        return average

    def updateQBar(self, action):
        average = 0
        numQHats = 0 # this should be the same as self.numSamples[action]
        for qHat in self.qHats[action]:
            average += qHat
            numQHats += 1
        average /= numQHats
        self.qBars[action] = average

        numSamples = self.numSamples[action]
        oldQBar = self.qBars[action]
        newQBar = oldQBar*(numSamples-1)
        newQBar += self.qHats[action][numSamples - 1]
        newQBar /= numSamples
        self.qBars[action] = newQBar

    def getVHat(self):
        return self.vHat


    def updateVHat(self):
        maxQBar = 0
        for qBar in self.qBars:
            if qBar > maxQBar:
                maxQBar = qBar
        self.vHat = maxQBar

    def getStarvingAction(self):
        maxStarve = self.budgetAlloc[0] - self.numSamples[0]
        bestAction = 0
        for action in self.actions:
            if self.budgetAlloc[action] - self.numSamples[action] > maxStarve:
                maxStarve = self.budgetAlloc[action] - self.numSamples[action]
                bestAction = action

        return bestAction


    def update(self, action, depth, depthBudget, initProbeBudget): # depth budget gives budget at each depth level
        positions = self.sampleY(action)
        # divide actions in two for now
        childState = OCBAState(positions=positions)
        if depth > 1:
            for sample in range(depthBudget[depth-1]):
                childState.OCBATree(depth - 1, depthBudget, initProbeBudget)
        else:
            childState.OCBATree(0, depthBudget, initProbeBudget) # this is handled by the numRewardSamples
        qHat = self.sampleReward() + childState.getVHat()
        self.qHats[action].append(qHat)
        self.numVisits = self.numVisits + 1
        self.numSamples[action] = self.numSamples[action]+1
        self.updateQBar(action)
        self.updateVariance(action)
        return


    def OCBATree(self, depth, depthBudget, initProbeBudget):  # returns vHat

        winVal = self.winCheck(self.positions)
        if winVal != -1:
            self.vHat = winVal
            return

        # winCheck = self.checkIfWinMove(self.positions, 1)
        # if winCheck != -1:
        #     self.vHat = 1
        #     return

        numRewardSamples = depthBudget[0]
        if depth == 0:
            # self.vHat = self.sampleRewardVHat(numRewardSamples) # make a sampleVHat function
            self.vHat = self.sampleVHat(numRewardSamples)
            return

        for action in self.actions: #for now, go through all of them
            if self.numSamples[action] < initProbeBudget:
                self.update(action, depth, depthBudget, initProbeBudget)
                self.updateVHat()
                return

        self.updateOptimalActions()
        for action in self.actions:
            self.updateKronecker(action)
        self.updateBudget()
        starvingAction = self.getStarvingAction()
        self.update(starvingAction, depth, depthBudget, initProbeBudget)
        self.updateVHat()
        self.updateOptimalActions()


    def showBoard(self):
        for y in range(6):
            for x in range(7):
                print(self.positions[x][5-y], end = ' ')
            print()

    def makeMove(self, action, whichPlayer): #assumes action is valid
        self.positions[action][self.actionHeight(self.positions, action)] = whichPlayer


