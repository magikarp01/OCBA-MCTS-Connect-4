from OCBA import OCBAState
from UCT import UCBState
import random
import array
"""
for x in range(5):
    checkPositions = [[0]*6, [0]*6, [1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [0]*6, [0]*6, [0]*6]
    root = state(positions = checkPositions, initProbeBudget=10) # initProbeBudget should be at least 2
    for x in range(20):
        root.UCBTree(1, 50) # depth does not work for >1 right now
    root.updateOptimalActions()
    print(root.getOptimalAction())
"""

# winningMovePositions = [[0]*6, [0]*6, [1, 1, 1, 0, 0, 0], [0]*6, [0]*6, [0]*6, [0]*6]
# checkState = state()
# print(checkState.checkIfWinMove(winningMovePositions, 1))


# initProbeBudget = int(input("Specify the initial probing budget n_0 (a good default would be 10): "))
# depth = int(input("Specify the depth of the branching (a good default would be 1): "))
# numRewardSamples = int(input("Specify the number of random rollouts performed per reward sample (a good default would be 20): "))
# budget = int(input("Specify the budget per move (a good default would be 20): "))

"""
testState = state()
#testPositions = [[0]*6, [0]*6, [0]*6, [2, 2, 1, 1, 2, 0], [1, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 2, 0, 0, 0, 0]]
testPositions = [[2, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [2, 1, 1, 0, 0, 0], [1, 2, 1, 0, 0, 0], [1, 2, 1, 2, 0, 0], [2, 2, 2, 1, 0, 0], [0]*6]
#winningMovePositions = [[2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [0]*6, [0]*6]
winningMovePositions = testPositions
#winningMovePositions = [[0] * 6 for _ in range(7)]
# print(testState.checkIfWinMove(winningMovePositions, 1))
# print(testState.checkIfWinMove(winningMovePositions, 2))
for test in range(100):
    rootState = state(positions= winningMovePositions)
    # print(rootState.sampleNext(winningMovePositions, 1))
    # print(rootState.sampleNext(winningMovePositions, 2))
    # print(rootState.rollout(42, 1))
    #print(rootState.sampleVHat(100))
    print(rootState.sampleY(2))
"""

def OCBAGame():
    initProbeBudget = 5
    depth = 1
    numRewardSamples = 10
    budget = 50

    # game = state([[1, 1, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0]*6, [0]*6])
    game = OCBAState()

    while game.winCheck(game.positions) == -1:
        root = OCBAState(positions=game.getPositions(), initProbeBudget=initProbeBudget, budget=budget)

        # print("before OCBA")
        # print(root.qBars)
        # print(root.qHats)
        # print(root.budgetAlloc)
        # print(root.numSamples)
        # print()
        for sample in range(budget):
            root.OCBATree(depth, numRewardSamples)
        root.updateOptimalActions()

        # print("after OCBA")
        print(root.qBars)
        print(root.qHats)
        print(root.budgetAlloc)
        print(root.numSamples)
        # print(root.positions)

        print("My move: ", end='')
        optAction = root.getOptimalAction()
        print(optAction + 1)
        game.makeMove(optAction, 1)
        game.showBoard()
        print()
        if game.winCheck(game.positions) != -1:
            break
        print("choose 1 through 7")
        selfAction = int(input("Your move: ")) - 1  # 0 to 6 representing columns
        game.makeMove(selfAction, 2)
        print()
        game.showBoard()
        print()

    if game.winCheck(game.positions) == 1:
        print("I win")

    elif game.winCheck(game.positions) == 0:
        print("You win")

    else:
        print("Draw")

def UCTGame():
    initProbeBudget=5
    depth=1
    numRewardSamples=20
    budget=50
    exploreParam = .1

    #game = state([[1, 1, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0]*6, [0]*6])
    game = UCBState()

    while game.winCheck(game.positions) == -1:
        root = UCBState(positions = game.getPositions(), budget = budget, initProbeBudget=initProbeBudget, exploreParam=exploreParam)

        for x in range(budget):
            root.UCBTree(depth, numRewardSamples)
        root.updateOptimalActions()

        print(root.qBars)
        print(root.numSamples)
        print(root.numVisits)
        print(root.UCBVals)

        print("My move: ", end='')
        optAction = root.getOptimalAction()
        print(optAction + 1)
        game.makeMove(optAction, 1)
        game.showBoard()
        print()
        if game.winCheck(game.positions) != -1:
            break

        while True:
            print("choose 1 through 7")
            try:
                selfAction = int(input("Your move: ")) - 1  # 0 to 6 representing columns
                if selfAction >= 0 and selfAction <= 6:
                    break
            except:
                pass

        game.makeMove(selfAction, 2)
        print()
        game.showBoard()
        print()

    if game.winCheck(game.positions) == 1:
        print("I win")

    elif game.winCheck(game.positions) == 0:
        print("You win")

    else:
        print("Draw")

#OCBAGame()
UCTGame()