from OCBA import OCBAState
from UCT import UCBState
import time
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


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
            print(x)

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

# OCBAGame(1, [10, 50], 5)
#UCBGame(2, [5, 20, 40], 2)

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

# playAgainst(1, [10, 50], 5, 2, 1)


# for x in range(1):
#     print("UCB First:")
#     playAgainst(1, [5, 50], 5, 2, 1)
#     print()
    # print("OCBA First:")
    # playAgainst(1, [5, 50], 5, 2, 2)
    # print()


def compare(depth, depthBudget, initProbeBudget, exploreParam, positions):
    UCB = UCBState(positions)
    OCBA = OCBAState(positions)

    UCBStart = time.time()
    for x in range(depthBudget[depth]):
        UCB.UCBTree(depth, depthBudget, exploreParam)
    UCBEnd = time.time()
    UCBTime = UCBEnd-UCBStart

    OCBAStart = time.time()
    for x in range(depthBudget[depth]):
        OCBA.OCBATree(depth, depthBudget, initProbeBudget)
    OCBAEnd = time.time()
    OCBATime = OCBAEnd - OCBAStart

    print("UCB: ")
    print(UCB.numSamples)
    print(UCB.qBars)
    print(UCB.getOptimalAction())
    print("UCB Time: " + str(UCBTime))


    print("OCBA: ")
    print(OCBA.numSamples)
    print(OCBA.qBars)
    print(OCBA.getOptimalAction())
    print("OCBA Time: " + str(OCBATime))



def comparePlotting(depth, depthBudget, initProbeBudget, exploreParam, positions):
    UCB = UCBState(positions)
    OCBA = OCBAState(positions)

    UCBActionQBars = [[], [], [], [], [], [], []]
    OCBAActionQBars = [[], [], [], [], [], [], []]

    UCBActionSamples = [[], [], [], [], [], [], []]
    OCBAActionSamples = [[], [], [], [], [], [], []]

    for x in tqdm(range(depthBudget[depth])):
        UCB.UCBTree(depth, depthBudget, exploreParam)
        OCBA.OCBATree(depth, depthBudget, initProbeBudget)
        # graph qBar against each action
        for action in range(7):
            UCBActionQBars[action].append(UCB.qBars[action])
            OCBAActionQBars[action].append(OCBA.qBars[action])
            UCBActionSamples[action].append(UCB.numSamples[action])
            OCBAActionSamples[action].append(OCBA.numSamples[action])

    iterations = range(depthBudget[depth])

    plt.subplots_adjust(hspace=.6, wspace=.3)
    plt.subplot(2, 2, 1)
    plt.title("UCB QBars")
    for action in range(7):
        plt.plot(iterations, UCBActionQBars[action], label = str(action))
    plt.legend()
    plt.xlabel("Iterations")
    plt.ylabel("Q-Bar")

    plt.subplot(2, 2, 2)
    plt.title("OCBA QBars")
    for action in range(7):
        plt.plot(iterations, OCBAActionQBars[action], label=str(action))
    plt.legend()
    plt.xlabel("Iterations")
    plt.ylabel("Q-Bar")


    plt.subplot(2, 2, 3)
    plt.title("UCB Samples")
    for action in range(7):
        plt.plot(iterations, UCBActionSamples[action], label=str(action))
    plt.legend()
    plt.xlabel("Iterations")
    plt.ylabel("Samples")

    plt.subplot(2, 2, 4)
    plt.title("OCBA Samples")
    for action in range(7):
        plt.plot(iterations, OCBAActionSamples[action], label=str(action))
    plt.legend()
    plt.xlabel("Iterations")
    plt.ylabel("Samples")

    plt.show()




testPositions1 = [[0]*6, [1, 1, 2, 2, 1, 0], [2, 1, 0, 0, 0, 0], [0]*6, [2, 1, 0, 0, 0, 0], [0]*6, [0]*6]
testPositions2 = [[0]*6, [0]*6, [0]*6, [0]*6, [0]*6, [0]*6, [0]*6]
#compareSampling(2, [5, 20, 40], 3, 2, testPositions)
comparePlotting(1, [5, 3000], 3, 2, testPositions2)