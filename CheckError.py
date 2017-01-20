import math
import numpy as np

imageBreadth = 1280
imageHeight = 1024


def checkError(V, M):
    lam = V[0]
    cx = V[1]
    cy = V[2]
    error = 0
    i = 0
    while i < len(M)-1:
        image = M[i]
        centeredImage = centerImagePixels(image, cx, cy)
        polarImage = pixelMatrixToPolar(centeredImage, lam)
        error += dotSumRoot(polarImage)
        i += + 30
    return error


def dotSumRoot(vectorMatrix):
    dotProducts = []

    # dot products for each row
    for i in range(6):  # rows
        cross = np.cross(vectorMatrix[i][0], vectorMatrix[i][-1])  # use the outer points
        norm = np.linalg.norm(cross, 2)

        cross = cross * (1 / norm)

        for j in range(1, 8 - 1):  # cols
            dot = np.dot(cross, vectorMatrix[i, j])
            dotProducts.append(dot)

    # dot product for each column
    for i in range(8):  # cols
        cross = np.cross(vectorMatrix[0, i], vectorMatrix[-1, i])
        norm = np.linalg.norm(cross, 2)

        cross = cross * (1 / norm)

        for j in range(1, 6 - 1):  # cols
            dot = np.dot(cross, vectorMatrix[j][i])
            dotProducts.append(dot)

    dotProducts = np.array(dotProducts)
    arcCosDots = np.arccos(dotProducts)
    sum = np.sum(arcCosDots)

    return sum


def centerImagePixels(M, cx, cy):
    Matrix = np.zeros((len(M), len(M[0]), 2))
    for i in range(len(M)):
        for j in range(len(M[0])):
            x, y = ImageToCam(M[i][j][0], M[i][j][1], cx, cy)
            Matrix[i][j] = [x, y]
    return Matrix


def pixelMatrixToPolar(M, lam):
    Matrix = np.zeros((len(M), len(M[0]), 3))

    for i in (range(len(M))):  # for each row
        for j in range(len(M[0])):  # for each col
            r = math.sqrt(math.pow(M[i][j][0], 2) + math.pow(M[i][j][1], 2))

            x = np.sin(lam * r) * (M[i][j][0] / r)
            y = np.sin(lam * r) * (M[i][j][1] / r)
            z = -(np.cos(lam * r))
            Matrix[i][j] = [x, y, z]

    return Matrix


def CamToImage(xs, ys, cx, cy):
    xi = xs + imageBreadth / 2 + cx
    yi = ys + imageHeight / 2 + cy

    return xi, yi


def ImageToCam(xi, yi, cx, cy):
    xs = xi - imageBreadth / 2 - cx
    ys = yi - imageHeight / 2 - cy

    return xs, ys


def runImageMatrix(M, filename):
    myfile = open(filename + ".csv", 'wb')
    myfile.write(bytes("Lambda,Error,\n", 'UTF-8'))
    MIN = 0.001 * math.pi / 1280.0
    MAX = 1.9 * math.pi / 1280.0
    # MIN = 0.00395
    # MAX = 0.00403
    STEPS = 1000
    DELTA = (MAX - MIN) / STEPS
    smallestError = float("inf")
    smallestLambda = 0

    cx = 69
    cy = -10
    output = ""
    for j in range(STEPS):
        if (j % 50 == 0):
            print("Processing step: " + str(j))
        lam = MIN + DELTA * j
        error = 0
        for i in range(0, (len(M) // 20)):
            matrix = pixelMatrixToPolar(M[i], lam)

            error += dotSumRoot(matrix)
        # error = error/lam
        output += str(lam) + "," + str(error) + ",\n"
        if (error < smallestError):
            smallestError = error
            smallestLambda = lam
    myfile.write(bytes(output, 'UTF-8'))
    myfile.close()

    print("Error: " + str(smallestError))
    print("Lamba: " + str(smallestLambda))


def pixelToPolarTrent(V, lam):
    #still using vector
    vector = np.zeros((len(V), 3))
    for i in (range(len(V))):
        x = np.sin(lam * (V[i][0] - cx)) * math.cos(lam * (V[i][1] - cy))
        y = np.sin(lam * (V[i][0] - cx)) * math.sin(lam * (V[i][1] - cy))
        z = np.cos(lam * (V[i][0] - cx))
        vector[i] = [x, y, z]
    # print(Vector)
    return vector