import ReadCheckerboard
import CheckError
import VerifyValues
import GradientDescent

LAMBDA = 0.00400232
# LAMBDA = 0.0025510322
# LAMBDA = 0.0032
[1.0046145  -69.27793205 -11.53974032]

# deminsions of checkerboard
cols = 8
rows = 6

cx = -69
cy = -10

imageBreadth = 1280
imageHeight = 1024

if __name__ == "__main__":
    points = ReadCheckerboard.loadPoints("data.pkl")
    #VerifyValues.verifyValues(points[1000], 0.004, -69, -10)
    #values = GradientDescent.gradientDescent(points, LAMBDA, cx, cy)
    #print(values)
    #VerifyValues.verifyValues(points[12], 0.0046145,  -69.27793205, -11.53974032)
    VerifyValues.makeImage("Results/checkerboard.jpg", 0.0046145,  -69.27793205, -11.53974032)