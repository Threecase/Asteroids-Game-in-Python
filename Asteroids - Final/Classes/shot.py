
import time, threading

class Shot(object):
    'Object for Shots'
    def __init__(self, canvas, x, y):
        self.c = canvas
        self.x = x
        self.y = y
        self.Time = 0
        self.dead = False
        
        self.draw(x,y)
        self.lifetime = self.Update(self)


    class Update(threading.Thread, object):
        def __init__(self, parent):
            threading.Thread.__init__(self, daemon=True, name='ShotUpdateThread')
            self.parent = parent
            self.start()

        def run(self):
            # Loop code
            while not self.parent.Time >= 2:
                self.parent.Time += 1
                time.sleep(1)
            self.parent.kill()



    def draw(self, x,y):
        # Do not run if shot has been killed
        if self.dead:
            return
        try:
            self.me
        except AttributeError:
            self.me = self.c.create_oval(x-2,y-2, x+2,y+2, fill='white',outline='white',tags=('shot'))
            
        self.x = x
        self.y = y
        try:
            self.c.coords(self.me, *(x-1,y-1,x+1,y+1))
        except ValueError:
            return


    def vector(self, x, y):
        playerPos = [self.x, self.y]
        mousePos = [x, y]
        vector = []
        for i in range(2):
            vector.append(playerPos[i] - mousePos[i])
        self.m = self.Move(self, vector[0], vector[1])



    class Move(threading.Thread, object):
        def __init__(self, parent, xVector, yVector):
            threading.Thread.__init__(self, daemon=True, name='ShotMoveThread')
            self.xVector = xVector
            self.yVector = yVector
            self.parent = parent
            self.start()

        def run(self):
            # Loop code
            while not self.parent.dead:
                newX = float(self.parent.x-(0.05*self.xVector))
                newY = float(self.parent.y-(0.05*self.yVector))

                if newX > 500:
                    newX = 1
                elif newX < 0:
                    newX = 499

                if newY > 500:
                    newY = 1
                elif newY < 0:
                    newY = 499
                    
                self.parent.draw(newX,newY)
                time.sleep(0.01)



    def kill(self):
        # Do not run if shot has been killed
        if self.dead:
            return
        self.dead = True
        self.m.join(1)
        self.c.delete(self.me)
