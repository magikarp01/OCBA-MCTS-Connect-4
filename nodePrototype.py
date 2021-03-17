# todo: limit the total number of calculations
# todo: implement batch sampling

import random
import math
from array import *
from copy import deepcopy

# i may need to have getters and setters
class state:
    def __init__(self, positions=[[0] * 6 for _ in range(7)], budget=0, initProbeBudget=0):
        self.positions = positions
        self.children = []
        self.totBudget = budget
        self.initProbeBudget = initProbeBudget
        self.setActions()

    # overall data
    positions = []
    numVisits = 0
    totBudget = 0
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
        return self.optimalActions[0]

    # run this at the very end
    def updateOptimalActions(self):
        maxQBar = self.qBars[0]
        optimalActions = [0]
        for action in self.actions:
            if self.qBars[action] > maxQBar:
                optimalActions = []
                optimalActions.append(action)
                maxQBar = self.qBars[action]
            elif self.qBars[action] == maxQBar:
                optimalActions.append(action)
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

        startAction = 0
        for action in self.actions:
            if action not in self.optimalActions:
                startAction = action
                break
        denom = self.variances[startAction] / (self.kroneckers[startAction] ** 2)

        ratios = [0] * 7

        for action in self.actions:
            if action in self.optimalActions:
                continue
            elif action == startAction:
                ratios[action] = 1
                continue
            else:  # assumes kroneckers and variances != 0
                ratio = self.variances[action] / (self.kroneckers[action] ** 2)
                ratio /= denom
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

        scale = (totBudget + 1) / total
        for action in range(7):
            budget[action] = scale * ratios[action]
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

    def checkIfLossMove(self, positions, action): #the only way a move could be a loss move is if the opponent wins on the same column
        positionsCopy = deepcopy(positions)
        actionHeight = self.actionHeight(positionsCopy, action)
        positionsCopy[action][actionHeight] = 1
        if positionsCopy[action][5] == 0:
            positionsCopy[action][actionHeight+1] = 2
        if self.winCheck(positionsCopy) == 0:
            return True # move is loss move
        return False


    def checkIfWinMove(self, positions): #prob needs to be more efficient
        for action in range(7):
            if positions[action][5] == 0:
                actionHeight = self.actionHeight(positions, action)
                positions[action][actionHeight] = 1

                if self.winCheck(positions) == 1:
                    return True
                else:
                    positions[action][actionHeight] = 0

        return False


    def rollout(self, numMoves, whichPlayer): #whichPlayer is 1 for self
        # get sample Q-hat by randomly simulating moves up to budget from parent
        # numMoves is total number of moves to make, max is 7*6 = 42
        # for now, every move is made uniformly random and we go to the end
        positions = self.getPositions()
        winVal = self.winCheck(positions)
        if winVal != -1:
            return winVal

        for move in range(numMoves):
            prevPositions = deepcopy(positions)

            # want to make winning move and don't want to make losing move
            if whichPlayer == 1:
                if self.checkIfWinMove(prevPositions):
                    return 1/(move+1)

            positions = self.sampleNext(positions, whichPlayer)
            #print(positions)

            winVal2 = self.winCheck(positions)
            if winVal2 != -1:
                return winVal2/(move+1)

            if whichPlayer == 2:
                whichPlayer = 1
            elif whichPlayer == 1:
                whichPlayer = 2

        return self.winHeuristic(positions)/numMoves


    def sampleY(self, action):
        positions = self.getPositions()
        positions[action][self.actionHeight(self.positions, action)] = 1
        positions = self.sampleNext(positions, 2)
        return positions

    def sampleReward(self, numRewardSamples): # how to make sure that longer games are not weighted higher?
        # currently, longer games have more stages and therefore will have higher total reward values
        # idea: divide the rollout return value by the number of moves until the game finished

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


    def update(self, action, depth, numRewardSamples):
        positions = self.sampleY(action)
        # fix budget
        childState = state(positions=positions, budget=0, initProbeBudget = self.initProbeBudget)
        childState.OCBATree(depth - 1, numRewardSamples)
        qHat = self.sampleReward(numRewardSamples) + childState.getVHat()
        self.qHats[action].append(qHat)
        self.numVisits = self.numVisits + 1
        self.numSamples[action] = self.numSamples[action]+1
        self.updateQBar(action)
        self.updateVariance(action)
        return


    def sampleRolloutVHat(self, numMoves, whichPlayer): # don't divide by numMoves here
        positions = self.getPositions()
        winVal = self.winCheck(positions)
        if winVal != -1:
            return winVal

        for move in range(numMoves):
            prevPositions = deepcopy(positions)

            # want to make winning move and don't want to make losing move
            if whichPlayer == 1:
                if self.checkIfWinMove(prevPositions):
                    return 1

            positions = self.sampleNext(positions, whichPlayer)
            # print(positions)

            winVal2 = self.winCheck(positions)
            if winVal2 != -1:
                return winVal2

            if whichPlayer == 2:
                whichPlayer = 1
            elif whichPlayer == 1:
                whichPlayer = 2

        return self.winHeuristic(positions)

    def sampleRewardVHat(self, numRewardSamples):
        average = 0
        for x in range(numRewardSamples):
            average += self.rollout(42, 1)
        average /= numRewardSamples
        return average


    def OCBATree(self, depth, numRewardSamples): #returns vHat
        #depth should probably be <3, 1 is probably good
        if self.checkHorizon(self.positions):
            self.numVisits = self.numVisits + 1 # probably wrong lol
            self.vHat = 0 # should I check if it's in a win/loss position?
            return

        winVal = self.winCheck(self.positions)
        if winVal != -1: # might overlap with checkHorizon
            self.vHat = winVal
            return

        if depth == 0:
            #self.vHat = self.sampleRewardVHat(numRewardSamples) # make a sampleVHat function
            self.vHat = self.sampleReward(numRewardSamples)
            return

        flag = True
        for action in self.actions: #for now, go through all of them
            if self.numSamples[action] < self.initProbeBudget:
                self.update(action, depth, numRewardSamples)
                self.updateVHat()
                if flag:
                    flag = False
                #return


        if flag:
            self.updateOptimalActions()
            for action in self.actions:
                self.updateKronecker(action)
            self.updateBudget()
            starvingAction = self.getStarvingAction()
            self.update(starvingAction, depth, numRewardSamples)
            self.updateVHat()


    def showBoard(self):
        for y in range(6):
            for x in range(7):
                print(self.positions[x][5-y], end = ' ')
            print()

    def makeMove(self, action, whichPlayer): #assumes action is valid
        self.positions[action][self.actionHeight(self.positions, action)] = whichPlayer