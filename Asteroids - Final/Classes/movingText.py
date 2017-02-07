
import time, threading, winsound, random

class MovingText(object):
    'Object for Moving Text'
    def __init__(self, canvas, x,y, text='TEXT', font=('Impact',50,'bold'), length=3):
        self.y = y
        self.c = canvas
        self.text = text
        self.font = font
        self.trailDict = {}
        self.threads = []
        self.col = ['red','orange','yellow','orange']
        winsound.PlaySound(random.choice([r"Sound\PrettyGood.wav",r"Sound\Wow.wav",r"Sound\Noice.wav",r"Sound\Nooo.wav"]),winsound.SND_FILENAME|winsound.SND_ASYNC)

        for i in range(length):
            self.trailDict[i] = canvas.create_text(x,y, text=text, font=font)
        
        c = 1
        cInc = 1
        for i in range(length):
            if c >= len(self.col)-1 or c <= 0:
                cInc = -cInc

            self.threads.append(threading.Thread(target=lambda: self.moveText(self.trailDict[i], (x+i),(y+i*2), inc=1, start=c),daemon=True))
            self.threads[i].start()

            c += cInc


    def moveText(self, t, x,y, inc=1, start=0):
        i = start
        iinc = 1
        it = 0
        while True:
            if y > self.y+(len(self.trailDict)*2) or y < self.y-(len(self.trailDict)):
                inc = -inc
            
            y += inc
            self.c.coords(t, x,y)
            self.c.itemconfig(t, fill=self.col[i])
            self.c.update()
            time.sleep(0.05)

            if it % 2 == 0:
                if i >= len(self.col)-1 or i < 0:
                    iinc = -iinc
                i += iinc
            it += 1
