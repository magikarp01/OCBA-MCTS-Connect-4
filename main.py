from Node import node
import random
import array

# startPos = [[0] * 6 for _ in range(7)]
# startPos[6][2] = 1
# print(startPos)
# print()
def showBoard(positions):
    for y in range(6):
        for x in range(7):
            print(positions[x][5-y], end=' ')
        print()

root = node()
positions = [[2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 1, 0, 0, 0, 0], [1, 2, 1, 2, 0, 0], [1, 2, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0]]


print(root.winCheck(positions))
showBoard(positions)

# print(root.winCheck([[2, 1, 2, 1, 1, 0], [2, 2, 2, 0, 0, 0], [1, 1, 2, 0, 0, 0], [2, 2, 0, 0, 0, 0], [2, 1, 1, 0, 0, 0], [1, 2, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0]]))
# showBoard([[2, 1, 2, 1, 1, 0], [2, 2, 2, 0, 0, 0], [1, 1, 2, 0, 0, 0], [2, 2, 0, 0, 0, 0], [2, 1, 1, 0, 0, 0], [1, 2, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0]])


# for test in range(100):
#     root = node([[0] * 6 for _ in range(7)], 0, 0)
#     print(root.getPositions())
#     # print(root.sampleNext(root.getPositions(), 1))
#     print(root.rollout(42, 1))
#     print()
    # print(random.randint(0, 7))
    # print(root.rollout(42, 1))