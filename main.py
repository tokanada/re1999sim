from multiprocessing import Process, Manager
import random
import matplotlib.pyplot as plt
import pandas as pd
import math
import warnings

warnings.filterwarnings('ignore')

# bluearchive 0.025
# aipura 0.035
# aipura 2x 0.07
fiveStarRate = 0.07
rateUpRates = [0.0075, 0.0075]
rateDownRate = .00144
standardFiveStarRate = round(fiveStarRate - sum(rateUpRates), 5)

# bluearchive 0.185
# aipura 0.15
fourStarTotalRate = 0.15
fourStarRate = 0.00882

# bluearchive 0.79
# aipura 0.815
# aipura 2x 0.78
threeStarTotalRate = 0.78
threeStarRate = 0.04794

tenPullCost = 2700


def generateCharacterPool():
    characterPool = ["Three Star", "Four Star", "Standard Five Star"]

    for i in range(1, len(rateUpRates) + 1):
        characterPool.append("Limited Five Star " + str(i))
    return characterPool


def calculateWeights():
    weights = [threeStarTotalRate, fourStarTotalRate, standardFiveStarRate]
    for rate in rateUpRates:
        weights.append(rate)
    return weights


def calculateTotalPoolRates(totalRate, individualRate):
    poolCount = round(totalRate / individualRate)
    return [individualRate] * poolCount


def calculatingFiveStarPoolSize():
    rateUpRateTotal = sum(rateUpRates)

    rateWithoutRateUp = round(fiveStarRate - rateUpRateTotal, 5)

    fiveStarPool = calculateTotalPoolRates(rateWithoutRateUp, rateDownRate)
    print("Total rate down five stars: " + str(len(fiveStarPool)))

    return fiveStarPool


def singlePullInstance(numberOfRolls):
    return random.choices(generateCharacterPool(), weights=calculateWeights(), k=numberOfRolls)


def multiplePullInstances(numberOfCycles, numberOfRolls):
    rollPool = []
    for i in range(0, numberOfCycles):
        rollPool.append(singlePullInstance(numberOfRolls))
    return rollPool


def parsePerRoll(totalPull, character):
    matchPerRoll = [0] * len(totalPull[0])
    for multiPull in totalPull:
        for pullIndex in range(len(multiPull)):
            if multiPull[pullIndex] == character:
                matchPerRoll[pullIndex] = matchPerRoll[pullIndex] + 1
    return matchPerRoll


def generateChart(numberOfCycles, numberOfRolls, characters):
    multiPull = multiplePullInstances(numberOfCycles, numberOfRolls)

    characterOccurencePerRollPosition = []
    for character in characters:
        characterOccurencePerRollPosition.append(parsePerRoll(multiPull, character))

    rollCount = list(range(1, numberOfRolls + 1))

    pullDataFrame = pd.DataFrame(characterOccurencePerRollPosition).T.set_axis(characters, axis=1)
    pullDataFrame['roll number'] = rollCount

    pullDataFrame.plot.bar(x='roll number', stacked=True, title='AIPURA Pull Success (All characters)', width=1)
    plt.show()

    pullDataFrameNoThreeStar = pullDataFrame.drop(labels='Three Star', axis=1)
    pullDataFrameNoThreeStar.plot.bar(x='roll number', stacked=True, title='AIPURA Pull Success (No 3 Stars)', width=1)
    plt.show()

    pullDataFrameOnlyFiveStars = pullDataFrameNoThreeStar.drop(labels='Four Star', axis=1)
    pullDataFrameOnlyFiveStars.plot.bar(x='roll number', stacked=True, title='AIPURA Pull Success (Only 5 Stars)',
                                        width=1)
    plt.show()

    pullDataFrameOnlyLimited = pullDataFrameOnlyFiveStars.drop(labels='Standard Five Star', axis=1)
    pullDataFrameOnlyLimited.plot.bar(x='roll number', stacked=True, title='AIPURA Limited Character Pull Success',
                                      width=1)
    plt.show()


# Unused for now
# fiveStarRateDownRates = calculatingFiveStarPoolSize()
# fourStarRates = calculateTotalPoolRates(fourStarTotalRate, fourStarRate)
# threeStarRates = calculateTotalPoolRates(threeStarTotalRate, threeStarRate)

def calculateNumberOfRolls(totalDiamonds, totalTickets):
    return (math.floor(totalDiamonds / tenPullCost) * 10) + totalTickets


def main():
    totalDiamonds = int(input("How many diamonds in total will you be spending? "))
    totalTickets = int(input("How many tickets will you be using? "))

    totalRolls = calculateNumberOfRolls(totalDiamonds, totalTickets)
    totalCycles = 1
    print("Total rolls (only counting 10 pulls @ 2700 diamonds per 10 pull) " + str(totalRolls))
    print("Running " + str(totalCycles) + " total rolling calculations")

    generateChart(totalCycles, totalRolls, generateCharacterPool())


main()