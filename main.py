import ReadCheckerboard
import CheckError
import VerifyValues
import GradientDescent
import cmath

# LAMBDA = 0.00400232
# LAMBDA = 0.0025510322
LAMBDA = cmath.pi/1000
cx = -8.46735397e+01
cy = -1.29954081e+01

V = [LAMBDA, cx, cy]
#V = [1.60683001e-03, -8.00110042e+01, -1.41146035e+01]
#V = [9.43838404e-03, 1.55423962e+02, -1.42297061e+02]
# dimensions of checkerboard
cols = 8
rows = 6

imageBreadth = 1280
imageHeight = 1024

if __name__ == "__main__":
    points = ReadCheckerboard.loadPoints("data.pkl")
    #values = GradientDescent.gradientDescent(points, LAMBDA, cx, cy)
    #print(values)

    frameNumber = 100
    VerifyValues.verifyValues(V, points[frameNumber])
    VerifyValues.displayVideoFrame("checkerboard.m4v", frameNumber, rows, cols)
    VerifyValues.makeImage(V, "frames/frame"+str(frameNumber)+".jpg")
