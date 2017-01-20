import numpy as np
import cv2
import pickle


def readCheckerbaord(path, rows, cols):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    video = cv2.VideoCapture(path)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print("File has " + str(length) + " frames")

    print("Beginning image scanning")
    i = 0
    while i < length - 1:

        if (i % 100 == 0):
            print(i)

        retval, img = video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            # cv2.drawChessboardCorners(img, (POINTS, ROWS), corners, ret)
            # cv2.imwrite('CheckerboardImages/result' + str(i) + '.jpg', img)
            # else:
            # print("pattern not found in image: " + str(i) + "\nSkipping to image: " + str(i + 10))
            # i += 10
            # video.set(1, i)
        i += 1

    Matrix = []
    for i in imgpoints:
        numpyVector = openCV2Numpy(i)
        Matrix.append(convertToTwoDArray(numpyVector, rows, cols))

    return Matrix


def convertToTwoDArray(V, rows, cols):
    matrix = np.zeros((rows, cols, 2))

    counter = 0
    for i in range(rows):
        for j in range(cols):
            matrix[i, j] = V[counter]
            counter += 1
    return matrix


def openCV2Numpy(V):
    vector = np.zeros((len(V), 2))
    for i in range(len(V)):
        x = V[i][0][0]
        y = V[i][0][1]
        vector[i] = [x, y]
    return vector


def pickleMatrix(M, filename):
    print("beginning pickle")
    with open(filename + '.pkl', 'wb') as output:
        pickle.dump(M, output, pickle.HIGHEST_PROTOCOL)


def loadPoints(filename):
    print("loading data points")
    with open(filename, 'rb') as input:
        newPoints = pickle.load(input)
    print("finished loading points")
    return newPoints
