
import threading, time, random

class Particle(object):
    'Object for Particles'
    def __init__(self, canvas, x,y, size):
        self.c = canvas
        self.x = x
        self.y = y
        self.size = size
        self.Time = 0
        self.dead = False
        self.me = self.c.create_oval(x-size,y-size, x+size,y+size, fill=random.choice(['red','yellow','orange']))
        self.vector = [random.randrange(-5,5)/2,random.randrange(-5,5)/2]
        
        self.draw(x,y)
        
        self.lt = self.Update(self)


    class Update(threading.Thread, object):
        def __init__(self, parent):
            threading.Thread.__init__(self, daemon=True, name='ParticleUpdateThread')
            self.inc = 0.01
            self.parent = parent
            self.start()

        def run(self):
            # Loop code
            while not self.parent.Time >= 1:
                self.parent.draw(self.parent.x+self.parent.vector[0],self.parent.y+self.parent.vector[1])
                time.sleep(self.inc)
                self.parent.Time += self.inc
            self.parent.kill()


    def draw(self, x,y):
        # Do not run if Particle has been killed
        if self.dead:
            return
        size = self.size/2
        self.x = x
        self.y = y

        try:
            self.c.coords(self.me, *(x-self.size,y-self.size, x+self.size,y+self.size))
        except ValueError:
            return


    def kill(self):
        # Do not run if Particle has been killed
        if self.dead:
            return
        self.dead = True
        self.c.delete(self.me)
