
from Classes import shot, particle
import time, threading, random

class Player(object):
    'Object for Player'
    def __init__(self, canvas, x,y, size):
        self.c = canvas
        self.size = size
        self.x = x
        self.y = y
        self.lastPos = [250,0]
        self.shots = []
        self.dead = False
        self.lives = 3
        self.mT = self.Move(0,0, self)
        
        self.draw(x,y)


    def draw(self, x,y):
        # Do not run if shot has been killed
        if self.dead:
            return
        size = self.size/2

        self.x = x
        self.y = y
        self.xy = [(x-size,y+size), (x,y+size/2), (x+size,y+size), (x,y-size)]

        try:
            self.me
        except AttributeError:
            self.me = self.c.create_polygon(self.xy, outline='white')

        coords = ()
        for i in self.xy:
            coords += i

        try:
            self.c.coords(self.me, *coords)
        except ValueError:
            return
        self.rotate(self.lastPos[0],self.lastPos[1])
        
        self.c.update()


    def vector(self, x,y):
        playerPos = [self.x, self.y]
        mousePos = [x, y]
        vector = []
        for i in range(2):
            vector.append(playerPos[i] - mousePos[i])

        self.lastPos = [mousePos[0],mousePos[1]]
        self.mT.xVector = vector[0]
        self.mT.yVector = vector[1]


    class Move(threading.Thread, object):
        def __init__(self, vectorX,vectorY, parent):
            threading.Thread.__init__(self, daemon=True, name='PlayerMoveThread')
            self.parent = parent
            self.xVector = vectorX
            self.yVector = vectorY
            self.start()
    
        def run(self):
            # Loop code
            while not self.parent.dead:
                while abs(self.xVector) > 0.1 and abs(self.yVector) > 0.1:
                    # teleport to other side if out of bounds
                    if self.parent.x > 500:
                        self.parent.x = 0
                    elif self.parent.x < 0:
                        self.parent.x = 500
                    if self.parent.y > 500:
                        self.parent.y = 0
                    elif self.parent.y < 0:
                        self.parent.y = 500

                    newX = self.parent.x-(0.05*self.xVector)
                    newY = self.parent.y-(0.05*self.yVector)
                    self.xVector = 0.99*self.xVector
                    self.yVector = 0.99*self.yVector

                    self.parent.draw(newX,newY)
        
                    time.sleep(0.01)
                time.sleep(0.07)


    def rotate(self, x,y):
        self.lastPos = [x, y]
        # calculate angle between cursor location and Player
        try:
            deltaX = self.c.canvasx(x) - self.x
            deltaY = self.c.canvasy(y) - self.y
        except ValueError:
            return

        try:
            angle = complex(deltaX, deltaY) / abs(complex(deltaX, deltaY))
        except ZeroDivisionError:
            angle = 0.0 # cannot determine angle

        angle = angle/-1j
        
        offset = complex(self.x, self.y)
        newxy = []
        for (x,y) in self.xy:
            v = angle * (complex(x, y) - offset) + offset
            newxy.append(v.real)
            newxy.append(v.imag)

        try:
            self.c.coords(self.me, *newxy)
        except ValueError:
            return


    def hitbox(self, x,y):
        inX = False
        inY = False

        if x <= self.x+self.size/2 and x >= self.x-self.size/2:
            inX = True
        if y <= self.y+self.size/2 and y >= self.y-self.size/2:
            inY = True

        if inX and inY:
            return True

        return False


    def shoot(self):
        # instantiate Shot at Player position
        self.shots.append(shot.Shot(self.c, self.x, self.y))


    def kill(self):
        # Do not run if Player has been killed
        if self.dead:
            return
        for i in range(15):
            particle.Particle(self.c, self.x,self.y, random.randrange(2,5))
        self.dead = (True if self.lives <= 0 else False)
        # if dead, delete self from canvas, remove all shots
        if self.dead:
            self.c.delete(self.me)
            self.shots = []
        # else reset the player
        else:
            self.mT.xVector = 0
            self.mT.yVector = 0
            self.x = 250
            self.y = 250
            self.draw(250,250)
        self.lives -= 1
