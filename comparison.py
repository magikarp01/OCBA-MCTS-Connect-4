from OCBA import OCBAState
from UCT import UCBState
import time

def OCBAGame(depth, depthBudget, initProbeBudget):
    game = OCBAState()

    while game.winCheck(game.positions) == -1:
        root = OCBAState(positions=game.getPositions())
        for sample in range(depthBudget[depth]):
            root.OCBATree(depth, depthBudget, initProbeBudget)
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

def UCBGame(depth, depthBudget, exploreParam):
    game = UCBState()

    while game.winCheck(game.positions) == -1:
        root = UCBState(positions=game.getPositions())

        for x in range(depthBudget[depth]):
            root.UCBTree(depth, depthBudget, exploreParam)
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

#OCBAGame(1, [10, 50], 5)
#UCBGame(1, [10, 50], 2)

def playAgainst(depth, depthBudget, initProbeBudget, exploreParam, whoFirst): # 1 for whoFirst is UCB first, 2 is OCBA first
    game = UCBState()
    if whoFirst == 1:
        while game.winCheck(game.positions) == -1:
            UCBPlayer = UCBState(positions=game.getPositions())
            for x in range(depthBudget[depth]):
                UCBPlayer.UCBTree(depth, depthBudget, exploreParam)
            UCBPlayer.updateOptimalActions()
            UCBAction = UCBPlayer.getOptimalAction()
            game.makeMove(UCBAction, 1)
            print("UCB Player:")
            game.showBoard()
            print(UCBPlayer.qBars)
            print(UCBPlayer.numSamples)
            print()
            # time.sleep(5)

            if game.winCheck(game.positions) != -1:
                print("UCB Player won")
                break

            OCBAPlayer = OCBAState(positions=game.getPositions())
            for x in range(depthBudget[depth]):
                OCBAPlayer.OCBATree(depth, depthBudget, initProbeBudget)
            OCBAAction = OCBAPlayer.getOptimalAction()
            game.makeMove(OCBAAction, 2)
            print("OCB Player:")
            game.showBoard()
            print(OCBAPlayer.qBars)
            print(OCBAPlayer.numSamples)
            print()
            # time.sleep(5)
            if game.winCheck(game.positions) != -1:
                print("OCBA Player won")
                break

    else:
        while game.winCheck(game.positions) == -1:
            OCBAPlayer = OCBAState(positions=game.getPositions())
            for x in range(depthBudget[depth]):
                OCBAPlayer.OCBATree(depth, depthBudget, initProbeBudget)
            OCBAAction = OCBAPlayer.getOptimalAction()
            game.makeMove(OCBAAction, 1)
            print("OCBA Player:")
            game.showBoard()
            print(OCBAPlayer.qBars)
            print(OCBAPlayer.numSamples)
            print()
            # time.sleep(5)
            if game.winCheck(game.positions) != -1:
                print("OCBA Player won")
                break

            UCBPlayer = UCBState(positions=game.getPositions())
            for x in range(depthBudget[depth]):
                UCBPlayer.UCBTree(depth, depthBudget, exploreParam)
            UCBPlayer.updateOptimalActions()
            UCBAction = UCBPlayer.getOptimalAction()
            game.makeMove(UCBAction, 2)
            print("UCB Player:")
            game.showBoard()
            print(UCBPlayer.qBars)
            print(UCBPlayer.numSamples)
            print()
            # time.sleep(5)

            if game.winCheck(game.positions) != -1:
                print("UCB Player won")
                break

playAgainst(1, [10, 50], 5, 2, 1)


# for x in range(1):
#     print("UCB First:")
#     playAgainst(1, [5, 50], 5, 2, 1)
#     print()
    # print("OCBA First:")
    # playAgainst(1, [5, 50], 5, 2, 2)
    # print()
# def timeCompare(positions): # not very useful: can make more efficient

#def samplingCompare(positions):
