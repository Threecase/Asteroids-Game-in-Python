#!/usr/bin/python3

'''
+--------------------------+
|         Asteroids        |     
| Last modified 2017-01-24 |
|      By Trevor Last      |
+--------------------------+
'''
from tkinter import*
from Classes import player as playerc, asteroid, shot, particle, movingText
import threading, random, time



# FUNCTIONS
def cleanup():
    m.destroy()
    quit(0)



class Update(threading.Thread, object):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True, name='MainUpdateThread')
        self.start()

    def run(self):
        # Init vars
        astList = []
        score = 0
        Time = 0
        scoreText = c.create_text(5,0, text='SCORE: %i'%score, font=('Impact',25,'bold'), anchor=NW, fill='white')
        livesText = c.create_text(5,30, text='LIVES: %i'%player.lives, font=('Impact',25,'bold'), anchor=NW, fill='white')

        # Loop code
        while not player.dead:
            if Time > 3:
                c.delete(title)
                c.delete(info)
            # Check that Asteroids exist
            if astList != []:
                # Loop through Asteroids
                for a in astList:
                    if a.dead:
                        continue
                    # Check Player
                    if a.hitbox(player.x,player.y):
                        player.kill()
                        c.delete('shot','asteroid')
                        astList = []
                        c.itemconfig(livesText, text='LIVES: %i'%player.lives)
                    # Check if Shots exist
                    if player.shots != []:
                        # Loop through Shots
                        for s in player.shots:
                            # Cleanup player.shots
                            if s.dead:
                                player.shots.remove(s)
                                continue
                            # Check hitbox, delete items that collide
                            if a.hitbox(s.x,s.y):
                                if a.size > 13:
                                    astList.append(createAsteroid(a.x,a.y, a.size/2))
                                astList.remove(a)
                                a.kill()
                                s.kill()
                                if a.size == 50:
                                    score += 20
                                elif a.size == 25:
                                    score += 50
                                else:
                                    score += 100
                                c.itemconfig(scoreText, text='SCORE: %i'%score)
                                if score % 10000 == 0:
                                    player.lives += 1
                                    c.itemconfig(livesText, text='LIVES: %i'%player.lives)
                                break
            
	    # Create Asteroids
            if len(astList) < 4:
                if random.randint(0,50) == 0:
                    x = random.randrange(0,500)
                    y = random.randrange(0,500)
                    # Make sure new asteroid is not created at same location as player
                    if player.hitbox(x,y):
                        x = random.randrange(0,500)
                        y = random.randrange(0,500)

                    astList.append(createAsteroid(x,y))

            Time += 0.01
            time.sleep(0.001)

        # Exit code
        # Delete the title screen, if it still exists
        c.delete(title)
        c.delete(info)
        c.itemconfig(livesText, text='LIVES: 0')

        # Add player's final score to score.txt
        if score > 0:
            with open('scores.txt','a') as scoreFile:
                scoreFile.write('\nScore: %i.'%score)

        # Read top scores from scores.txt
        with open('scores.txt','r') as scoreFile:
            scores = ''
            for l in scoreFile.read():
                if l in '0123456789':
                    scores += l
                if l == '.':
                    scores += l

        # Configure scores list for proper reading
        scores = scores.split('.')
        scores.remove(scores[len(scores)-1])
        for i in range(len(scores)):
            scores[i] = int(scores[i])

        # If there aren't 3 scores, display all of them
        r = 3
        if not len(scores) >= 3:
            r = len(scores)

        # insert the top 3 scores into a list --TODO: CHANGE LIST TO DICT, DISPLAY NAME
        topScores = []
        for i in range(r):
            topScores.append(str(max(scores))+', ')
            ind = scores.index(max(scores))
            scores.remove(scores[ind])

        # Display text
        movingText.MovingText(c, 250,125, text='TOP SCORES: '+''.join(topScores), font=('Impact',30))
        c.create_text(250,250, text='Final Score: %i'%score, font=('Impact',50), fill='white')
        c.create_text(250,400, text='GAME OVER', font=('Impact',80,'bold'), fill='white')
        time.sleep(3)
        return cleanup()


def createAsteroid(x,y, size=50):
    return asteroid.Asteroid(c, x,y, size, random.randrange(0,2))


def rotation(event):
    player.rotate(event.x, event.y)


def movement(event):
    player.vector(event.x, event.y)
    c.delete(title)
    c.delete(info)


def shoot(event):
    player.shoot()
    player.shots[len(player.shots)-1].vector(event.x,event.y)
# END FUNCTIONS



# TKINTER
m = Tk()
m.title('Game')
m.bind('<Button-1>',shoot)
m.bind('w', movement)
m.bind('<Motion>',rotation)
m.bind('<Escape>',lambda e:cleanup())
m.protocol('WM_CLOSE_WINDOW',lambda:cleanup())

c = Canvas(m,width=500,height=500,bg='black')
c.pack(expand=True)
# END TKINTER



# MAIN
player = playerc.Player(c, 250,250, 25)

title = c.create_text(250,150, text='ASTEROIDS', font=('Impact',75,'bold'), fill='white')
info = c.create_text(250,300, justify=CENTER,
                     text='To fire, left click.\nTo move, press "w".\nThe escape key will close the window.',
                     font=('Impact',15), fill='white')



Update()
m.mainloop()
