from nodePrototype import state
import random
import array
"""
for x in range(5):
    checkPositions = [[0]*6, [0]*6, [1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [0]*6, [0]*6, [0]*6]
    root = state(positions = checkPositions, initProbeBudget=10) # initProbeBudget should be at least 2
    for x in range(20):
        root.OCBATree(1, 50) # depth does not work for >1 right now
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


testState = state()
winningMovePositions = [[2, 0, 0, 0, 0, 0], [1, 1, 1, 2, 0, 0], [1, 0, 0, 0, 0, 0], [1, 2, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [0]*6, [0]*6]
print(testState.checkIfWinMove(winningMovePositions))
print(testState.checkIfLossMove(winningMovePositions, 2))
for test in range(1000):
    print(testState.sampleNext(winningMovePositions, 1))


initProbeBudget=3
depth=1
numRewardSamples=20
budget=3

game = state()

while game.winCheck(game.positions) == -1:
    root = state(positions = game.getPositions(), initProbeBudget=initProbeBudget)
    for x in range(budget):
        root.OCBATree(depth, numRewardSamples)
    root.updateOptimalActions()
    print("My move: ", end='')
    optAction = root.getOptimalAction()
    print(optAction)
    game.makeMove(optAction, 1)
    game.showBoard()
    print()
    if game.winCheck(game.positions) != -1:
        break

    selfAction = int(input("Your move: ")) # 0 to 6 representing columns
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