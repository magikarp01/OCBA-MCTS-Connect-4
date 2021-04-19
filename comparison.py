from OCBA import OCBAState
from UCT import UCBState

def OCBAGame(initProbeBudget, depth, depthBudget):
    game = OCBAState()

    while game.winCheck(game.positions) == -1:
        root = OCBAState(positions=game.getPositions(), initProbeBudget=initProbeBudget)
        for sample in range(depthBudget[depth]):
            root.OCBATree(depth, depthBudget)
        root.updateOptimalActions()

        print(root.qBars)
        # print(root.qHats)
        # print(root.budgetAlloc)
        # print(root.numSamples)

        print("My move: ", end='')
        optAction = root.getOptimalAction()
        print(optAction + 1)
        game.makeMove(optAction, 1)
        game.showBoard()
        print()
        if game.winCheck(game.positions) != -1:
            break
        print("choose 1 through 7")
        selfAction = int(input("Your move: ")) - 1
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

def UCTGame(depth, depthBudget, exploreParam):
    game = UCBState()

    while game.winCheck(game.positions) == -1:
        root = UCBState(positions=game.getPositions(), exploreParam=exploreParam)

        for x in range(depthBudget[depth]):
            root.UCBTree(depth, depthBudget)
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

#OCBAGame(5, 1, [10, 50])
UCTGame(1, [10, 50], .1)