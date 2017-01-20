import cv2
import numpy as np
import CheckError
from PIL import Image, ImageDraw
import math


def verifyValues(M, lam, cx, cy):

    M = CheckError.centerImagePixels(M, cx, cy)
    matrix = np.zeros((len(M), len(M[0]), 3))
    for i in range(len(M)):
        for j in range(len(M[0])):
            x, y, z = projectPixel(lam, M[i][j][0], M[i][j][1])
            matrix[i][j] = [x, y, x]
    image = Image.new("RGB", (2000, 2000), "white")
    draw = ImageDraw.Draw(image)

    for i in matrix:
        for j in range(len(i)-1):
            x1 = (i[j][0]) * 100 + 1000
            y1 = (i[j][1]) * 100 + 1000

            x2 = i[j + 1][0] * 100 + 1000
            y2 = i[j + 1][1] * 100 + 1000

            if x1 < 2000 and x1 > 0 and y1 < 2000 and y1 > 0:
                if x2 < 2000 and x2 > 0 and y2 < 2000 and y2 > 0:
                    draw.line(((x1, y1), (x2, y2)), fill=128)

    image.show()


def buildRGBArray(filename):
    im = Image.open(filename)
    width, height = im.size
    rgb_im = im.convert('RGB')
    M = np.zeros((width, height, 3))
    for i in range(width):
        for j in range(height):
            r, g, b = rgb_im.getpixel((i, j))
            M[i, j] = [r, g, b]
    return M


def makeImage(filename, lam, cx, cy):
    M = buildRGBArray(filename)
    image = Image.new("RGB", (2000, 2000), "white")
    pix = image.load()
    error = 0
    for i in range(1, len(M)):
        for j in range(1, len(M[i])):
            ix, iy = CheckError.ImageToCam(i, j, cx, cy)
            x, y, z = projectPixel(lam, ix, iy)

            #x, y = CheckError.CamToImage(x, y, cx, cy)
            x = x * 100 + 1000
            y = y * 100 + 1000

            if (x < 2000 and x > 0 and y < 2000 and y > 0 and z < 0):
                pix[x, y] = (int(M[i, j, 0]), int(M[i, j, 1]), int(M[i, j, 2]))
            else:
                error += 1
    print(error)
    image.show()


def projectPixel(lam, _x, _y):
    r = math.sqrt(math.pow(_x, 2) + math.pow(_y, 2))
    if r == 0:
        return 0, 0, 0
    x = np.sin(lam * r) * (_x / r)
    y = np.sin(lam * r) * (_y / r)
    z = -(np.cos(lam * r))
    return x / -z, y / -z, z


def displayVideoFrame(path, frameNumber, rows, cols):
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
    while i <= frameNumber:
        retval, img = video.read()
        if i == frameNumber:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None)

            # If found, add object points, image points (after refining them)
            if ret:
                objpoints.append(objp)

                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

                # Draw and display the corners

                cv2.drawChessboardCorners(img, (cols, rows), corners, ret)
                cv2.imwrite('frame' + str(i) + '.jpg', img)
                # else:
                # print("pattern not found in image: " + str(i) + "\nSkipping to image: " + str(i + 10))
                # i += 10
                # video.set(1, i)
        i += 1