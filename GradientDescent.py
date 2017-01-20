import CheckError
import copy
import scipy.optimize
import numpy as np


def gradientDescent(M, lam, cx, cy):
    x0 = np.array([lam, cx, cy])
    tup = tuple(([M]))
    res = scipy.optimize.fmin_powell(CheckError.checkError, x0, args=(tup))
    return res


def badGradientDescent(M, lam, cx, cy):
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
