from math import *
from array import *
from time import sleep
import sys

dice1 = ["A", "B", "C"]
dice2 = ["D", "E", "F"]
dice3 = ["G", "H", "I"]
allDice = [dice1, dice2, dice3]
dice = {}

for i, face1 in enumerate(dice1):
    for j, face2 in enumerate(dice2):
        for k, face3 in enumerate(dice3):
            dice[i * 9 + j * 3 + k] = {"M": [], "F": [face1, face2, face3]}

InteractionTypes = {
    tuple[1, 1, 0]: 6,  # 1B2B3
    tuple[1, 0, 0]: 3,  # 1B3B2
    tuple[0, 1, 0]: 3,  # 2B1B3
    tuple[0, 1, 1]: 6,  # 2B3B1
    tuple[1, 0, 1]: 6,  # 3B1B2
    tuple[0, 0, 1]: 3,  # 3B2B1
}

OneB2B3 = 6
OneB3B2 = 3
TwoB1B3 = 3
TwoB3B1 = 6
ThreeB1B2 = 6
ThreeB2B1 = 3

OneBeatsTwo = 15
OneBeatsThree = 12
TwoBeatsOne = 12
TwoBeatsThree = 15
ThreeBeatsOne = 15
ThreeBeatsTwo = 12

dice[0]["M"] = [0, 1, 2]

print(
    f"{dice[0]['F'][dice[0]['M'][0]]} beats {dice[0]['F'][dice[0]['M'][1]]} which beats {dice[0]['F'][dice[0]['M'][2]]}"
)


# class node:
#     def __init__(self, name):
#         self.name = name
#         self.leftInteractions = []
#         self.rightInterations = []

#     def addInteration(self, node, direction):
#         if direction == "left":
#             self.leftInteractions.append(node)
#         elif direction == "right":
#             self.rightInterations.append(node)

#     def getInteraction(self, direction):
#         if direction == "left":
#             return self.leftInteractions
#         elif direction == "right":
#             return self.rightInterations

#     def removeInteraction(self, node, direction):
#         if direction == "left":
#             self.leftInteractions.remove(node)
#         elif direction == "right":
#             self.rightInterations.remove(node)

#     def __str__(self):
#         return self.name


# Ad = node("A")
# Bd = node("B")
# Cd = node("C")
# Dd = node("D")
# Ed = node("E")
# Fd = node("F")
# Gd = node("G")
# Hd = node("H")
# Id = node("I")


def setsThatContain(first, second):
    def getDiceRange(diceInput):
        if diceInput[0] == 0:
            returnRange = list(range(diceInput[1] * 9, diceInput[1] * 9 + 9))
        elif diceInput[0] == 1:
            returnRange = []
            returnRange.extend(list(range(diceInput[1] * 3, diceInput[1] * 3 + 3)))
            returnRange.extend(list(range(diceInput[1] * 3 + 9, diceInput[1] * 3 + 12)))
            returnRange.extend(
                list(range(diceInput[1] * 3 + 18, diceInput[1] * 9 + 21))
            )
        elif diceInput[0] == 2:
            returnRange = list(range(diceInput[1], diceInput[1] + 25, 3))

        return returnRange

    for i, dice in enumerate(allDice):
        if first in dice:
            firstDice = [i, dice.index(first)]
        if second in dice:
            secondDice = [i, dice.index(second)]

    set1 = set(getDiceRange(firstDice))
    set2 = set(getDiceRange(secondDice))

    returnList = list(set1.intersection(set2))
    returnList.sort()
    return returnList


testVar = setsThatContain("A", "F")
print(testVar)


DiceInteractions = [[None] * 27 for i in range(3)]

DiceInteractions[0][0] = 1
DiceInteractions[1][0] = 1
DiceInteractions[2][0] = 0


def updateInteractions(interactionRow, interactionColumn):
    global DiceInteractions

    # Get the indexes of the dice face combinations that contain the interacting faces
    overlap = setsThatContain(
        dice[interactionRow]["F"][interactionColumn],
        dice[interactionRow]["F"][interactionColumn - 2],
    )

    # Iterate through the list of indexes and set the interaction to the same as the first
    for i in overlap:
        DiceInteractions[interactionColumn][i] = DiceInteractions[interactionColumn][
            interactionRow
        ]


def checkInteractions():
    for i in range(27):
        for j in range(3):
            if DiceInteractions[j][i] != None:
                updateInteractions(i, j)


def checkBucket(interactionRow):
    if interactionRow == [1, 1, 0]:
        return "OneB2B3"
    elif interactionRow == [1, 0, 0]:
        return "OneB3B2"
    elif interactionRow == [0, 1, 0]:
        return "TwoB1B3"
    elif interactionRow == [0, 1, 1]:
        return "TwoB3B1"
    elif interactionRow == [1, 0, 1]:
        return "ThreeB1B2"
    elif interactionRow == [0, 0, 1]:
        return "ThreeB2B1"


def checkForSolutions(printSolutions=False):
    updateCount = 0
    while updateCount <= 1:
        for i in range(27):
            noneCount = 0
            noneIndex = None
            for j in range(3):
                if DiceInteractions[j][i] == None:
                    noneIndex = j
                    noneCount += 1

            if noneCount == 0:
                # get the type of interaction and see if we can afford it from the interaction buckets

                # if a bucket runs out of room, go back to the previous branch point and try something else
                pass

            elif noneCount == 1:
                tempSet = {
                    DiceInteractions[j][i],
                    DiceInteractions[j - 1][i],
                    DiceInteractions[j - 2][i],
                }
                tempSet.remove(None)
                if len(tempSet) == 1:
                    if tempSet.pop() == 1:
                        DiceInteractions[noneIndex][i] = 0
                    else:
                        DiceInteractions[noneIndex][i] = 1

                    checkInteractions()

                    updateCount = 0
                    break

        updateCount += 1


checkInteractions()
checkForSolutions()

DiceInteractions[0][17] = 0
checkInteractions()
checkForSolutions()
DiceInteractions[1][17] = 0
checkInteractions()
checkForSolutions()
DiceInteractions[2][17] = 1
checkInteractions()
checkForSolutions()

DiceInteractions[0][8] = 0
checkInteractions()
checkForSolutions()

DiceInteractions[0][9] = 1
checkInteractions()
checkForSolutions()

DiceInteractions[2][26] = 1
checkInteractions()
checkForSolutions()

DiceInteractions[2][1] = 0
checkInteractions()
checkForSolutions()


def branch(value):
    updateCount = 0
    while updateCount <= 1:
        for i in range(27):
            noneCount = 0
            noneIndex = None
            for j in range(3):
                if DiceInteractions[j][i] == None:
                    noneIndex = j
                    noneCount += 1

            if noneCount == 1:
                tempSet = {
                    DiceInteractions[j][i],
                    DiceInteractions[j - 1][i],
                    DiceInteractions[j - 2][i],
                }
                tempSet.remove(None)
                if len(tempSet) == 2:
                    DiceInteractionsCopy = DiceInteractions.copy()
                    branch(1)
                    #    DiceInteractions[noneIndex][i] = 0
                    branch(2)
                    #    DiceInteractions[noneIndex][i] = 1

                    checkInteractions()

                    updateCount = 0
                    break


for column in DiceInteractions:
    for row in column:
        print(f"{str(row): <5}", end="")
    print()

print(InteractionTypes[tuple[0, 1, 1]])
