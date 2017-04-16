
from . import particle
import threading, time, random, math

class Asteroid(object):
    'Object for Asteroids'
    def __init__(self, canvas, x,y, size, shape=1):
        self.c = canvas
        self.x = x
        self.y = y
        self.size = size
        self.type = shape
        self.dead = False

        self.draw(x,y)
        self.m = self.Move(self, random.randrange(-5,5),random.randrange(-5,5))


    def draw(self, x,y):
        # Do not run if Asteroid has been killed
        if self.dead:
            return
        size = self.size/2
        # three possible shapes
        type0 = [(x+size/3,y-size), (x-size/3,y-size), (x-size/4,y-size/2), (x-size,y-size/2), (x-size,y+size/6), (x-size/2,y+size/1.1), (x+size/4,y+size/1.5), (x+size/2,y+size), (x+size,y+size/2), (x+size/3,y), (x+size,y-size/3), (x+size,y-size/2)]
        type1 = [(x+size/2,y-size/1.1), (x,y-size), (x-size/1.5,y-size/1.5), (x-size,y), (x-size/1.7,y+size/1.5), (x,y+size), (x+size/6,y+size/1.7), (x+size/1.2,y+size/1.4), (x+size,y), (x+size/2,y-size/4)]
        type2 = [(x+size/3,y-size), (x-size/3,y-size), (x-size,y-size/3), (x-size/3,y), (x-size,y+size/3), (x-size/4,y+size), (x,y+size/4), (x,y+size), (x+size/3,y+size), (x+size,y+size/3), (x+size,y-size/3)]
        self.types = [type0, type1, type2]

        self.xy = self.types[self.type]
        try:
            self.me
        except AttributeError:
            self.me = self.c.create_polygon(self.xy,outline='white',tags=('asteroid'))

        coord = ()
        for i in self.xy:
            coord += i

        self.x = x
        self.y = y

        try:
            self.c.coords(self.me, *coord)
        except ValueError:
            return

        self.rotate()
        self.c.update()


    class Move(threading.Thread, object):
        def __init__(self, parent, vectorX,vectorY):
            threading.Thread.__init__(self, daemon=True, name='AsteroidMoveThread')
            self.parent = parent
            if vectorX == 0:
                vectorX = random.randrange(-5,5)
            if vectorY == 0:
                vectorY = random.randrange(-5,5)
            self.vectorX = vectorX
            self.vectorY = vectorY
            self.start()
    
        def run(self):
            # Loop code
            while not self.parent.dead:
                # teleport to other side if out of bounds
                if self.parent.x > 500:
                    self.parent.x = 0
                elif self.parent.x < 0:
                    self.parent.x = 500
                if self.parent.y > 500:
                    self.parent.y = 0
                elif self.parent.y < 0:
                    self.parent.y = 500

                newX = self.parent.x-(0.25*self.vectorX)
                newY = self.parent.y-(0.25*self.vectorY)

                self.parent.draw(newX,newY)
        
                time.sleep(0.01)


    def rotate(self):
        # Do not run if asteroid has been killed
        if self.dead:
            return

        # calculate angle between cursor location and Player
        try:
            deltaX = self.c.canvasx(250) - self.x
            deltaY = self.c.canvasy(250) - self.y

            try:
                angle = complex(deltaX, deltaY) / abs(complex(deltaX, deltaY))
            except ZeroDivisionError:
                angle = 0.0 # cannot determine angle

            angle = angle/-1j
        
            offset = complex(self.x, self.y)
            newxy = []
            for (x, y) in self.xy:
                v = angle * (complex(x, y) - offset) + offset
                newxy.append(v.real)
                newxy.append(v.imag)
            self.c.coords(self.me, *newxy)
        except:
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


    def kill(self):
        # Do not run if Asteroid has been killed
        if self.dead:
            return
        for i in range(10):
            particle.Particle(self.c, self.x,self.y, size=random.randrange(1,5))
        self.dead = True
        self.m.join(1)
        self.c.delete(self.me)
