import CheckError
import copy
import scipy.optimize
import numpy as np
import math


def gradientDescent(M, lam, cx, cy):
    #x0 = np.array([lam, cx, cy])

    min = math.pi - math.pi/1000
    max = math.pi + math.pi/1000

    bounds = [(min, max), (-100, 100), (-20, 20)]
    tup = tuple(([M]))
    res = scipy.optimize.differential_evolution(CheckError.checkError, bounds, tup)
    return res


def fprime(x0, M):
    lam = x0[0]
    cx = x0[1]
    cy = x0[2]

    results = []

    # todo: code better
    deltaLam = lam / 100
    error1 = CheckError.checkError([lam + deltaLam, cx, cy], M)
    error2 = CheckError.checkError([lam - deltaLam, cx, cy], M)
    results.append(gradient(error1, error2, deltaLam))

    deltaCx = cx / 100
    error1 = CheckError.checkError([lam, cx + deltaCx, cy], M)
    error2 = CheckError.checkError([lam, cx - deltaCx, cy], M)
    results.append(gradient(error1, error2, deltaCx))

    deltaCy = cy / 100
    error1 = CheckError.checkError([lam, cx, cy + deltaCy], M)
    error2 = CheckError.checkError([lam, cx, cy - deltaCy], M)
    results.append(gradient(error1, error2, deltaCy))

    return np.array(results)


def gradient(error1, error2, delta):
    return ((error1 - error2) / 2 * delta)


def hillClimbing(M, lam, cx, cy):
    currentValues = [lam, cx, cy]
    smallestValues = []
    smallestError = float("inf")
    while 1:
        for i in range(3):
            step = currentValues[i] / 1000

            testValues = copy.deepcopy(currentValues)
            testValues[i] = testValues[i] - step
            error = CheckError.checkError(M, testValues[0])
            if error < smallestError:
                smallestValues = copy.deepcopy(testValues)
                smallestError = error

            testValues[i] = testValues[i] + step * 2
            error = CheckError.checkError(M, testValues[0])
            if error < smallestError:
                smallestValues = copy.deepcopy(testValues)
                smallestError = error

        if currentValues[0] == smallestValues[0] and currentValues[1] == smallestValues[1] and currentValues[2] == \
                smallestValues[2]:
            break
        currentValues = copy.deepcopy(smallestValues)
    return currentValues
