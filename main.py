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

game = state()

while game.winCheck(game.positions) == -1:
    root = state(positions = game.getPositions(), initProbeBudget=10)
    for x in range(20):
        root.OCBATree(1, 20)
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
