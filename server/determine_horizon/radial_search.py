import math

# smart search adjustment
def detMaxElevation(latitude, longitude):
    if 35 < latitude < 72 and -25 < longitude < 65:
        return 6000

def determineSearchRadius(elevation, latitude, longitude):
    distToHorizon = (math.acos(6367500 / (6367500 + elevation)) * 40008180) / math.tau
    distToElevation = (math.acos(6367500 / (6367500 + detMaxElevation(latitude, longitude))) * 40008180) / math.tau
    print(distToHorizon, distToElevation)
    return distToElevation + distToHorizon

print(determineSearchRadius(250, 45, 20), "m")
