import math
import numpy as np

imageBreadth = 1280
imageHeight = 1024


def checkError(V, M):
    lam = V[0]
    cx = V[1]
    cy = V[2]
    totalError = 0
    for image in M[:50]:
        centeredImage = centerImagePixels(image, cx, cy)
        polarImage = pixelMatrixToPolar(centeredImage, lam)
        error = dotSumRoot(polarImage)
        totalError += error
    return math.sqrt(totalError)


def dotSumRoot(vectorMatrix):
    dotProducts = []
    # dot products for each row
    for i in vectorMatrix:
        cross = np.cross(i[0], i[-1])  # use the outer points
        norm = np.linalg.norm(cross, 2)

        cross = cross * (1 / norm)

        for j in i[1:-1]:
            dot = np.dot(cross, j)
            dotProducts.append(dot)

    # dot product for each column

    vectorMatrixT = np.transpose(vectorMatrix, (1, 0, 2))
    for i in vectorMatrixT:
        cross = np.cross(i[0], i[-1])  # use the outer points
        norm = np.linalg.norm(cross, 2)

        cross = cross * (1 / norm)

        for j in i[1:-1]:
            dot = np.dot(cross, j)
            dotProducts.append(dot)

    dotProducts = np.array(dotProducts)
    arcCosDots = np.arccos(dotProducts)
    square = np.power(arcCosDots, 2)
    sum = np.sum(square)

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
            r = math.sqrt(math.pow(M[i][j][0], 2.0) + math.pow(M[i][j][1], 2.0))

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
    xs = xi - (imageBreadth / 2) - cx
    ys = yi - (imageHeight / 2) - cy

    return xs, ys


def runImageMatrix(M, filename):
    myfile = open(filename + ".csv", 'wb')
    myfile.write(bytes("Lambda,Error,\n", 'UTF-8'))
    MIN = 0.001 * math.pi / 1280.0
    MAX = 1.9 * math.pi / 1280.0
    # MIN = 0.001
    # MAX = 0.002
    STEPS = 1000
    DELTA = (MAX - MIN) / STEPS
    smallestError = float("inf")
    smallestLambda = 0

    cx = -8.46735397e+01
    cy = -1.29954081e+01
    output = ""
    for j in range(STEPS):
        if (j % 50 == 0):
            print("Processing step: " + str(j))
        lam = MIN + DELTA * j
        V = [lam, cx, cy]
        error = checkError(V, M)
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
    # still using vector
    vector = np.zeros((len(V), 3))
    for i in (range(len(V))):
        x = np.sin(lam * (V[i][0] - cx)) * math.cos(lam * (V[i][1] - cy))
        y = np.sin(lam * (V[i][0] - cx)) * math.sin(lam * (V[i][1] - cy))
        z = np.cos(lam * (V[i][0] - cx))
        vector[i] = [x, y, z]
    # print(Vector)
    return vector
