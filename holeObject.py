from graphics import *

#Class for instance object Hole
class Hole(object):

    #constructor
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.r = radius
        self.c = 0 #initialize self.c for circle/shape object holding

    #takes in instance of self, and window
    #creates circle from Hole info, and draws to window.
    def makeHole(self, win):
        self.c = Circle(self.getPoint(), self.r)
        self.c.setFill('brown')
        self.c.draw(win)

    #undraw Hole on window
    def undrawHole(self):
        self.c.undraw()

    #Hole is made with separate x and y variables.
    #This combines the x and y into a Point.
    def getPoint(self):
        p = Point(self.x, self.y)
        return p

    #Checks distance between a point and a Hole center.
    #Returns True if the distance is less than Hole radius.
    def checkPoints(self, point1): # modified from bounce2.py getShift
        dx = self.x - point1.getX()
        dy = self.y - point1.getY()

        #Pythagorean Theorem
        distance = (dx*dx + dy*dy)**0.5

        if (distance <= self.r):
            return True
        else:
            return False

    #Checks distance between two holes.
    #Similar to checkPoints, but this accounts for radius distances.
    #Return True if distance between both centers <= both radiuses added
    def checkCircles(self, hole): # modified from bounce2.py
        dx = self.x - hole.x
        dy = self.y - hole.y

        distance = (dx*dx + dy*dy)**0.5

        if (distance <= (self.r + hole.r)):
            return True
        else:
            return False
