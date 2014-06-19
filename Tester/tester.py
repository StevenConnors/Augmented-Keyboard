# events-example1-no-globals.py
# Demos timer, mouse, and keyboard events

# Search for "DK" in comments for all the changes
# required to eliminate globals.

from Tkinter import *
import math
import time
import string
import datetime
import tkFileDialog

def mousePressed(canvas, event):
    data=canvas.data
    if data.start:
#        print data.clicks
        if ( ((event.x-data.centerX)**2)+((event.y-data.centerY)**2)<\
                ((data.circleWidth/2)**2) ):
            canvas.data.listcX.append(canvas.data.centerX)
            canvas.data.listcY.append(canvas.data.centerY)
            canvas.data.clicks+=1
            recordTime(canvas)
            resetPath(canvas)
        else: #clicked outside of the circle
            errorX=event.x-canvas.data.centerX
            errorY=event.y-canvas.data.centerY
            canvas.data.error.append(canvas.data.clicks)
#            print (canvas.da'.ta.clicks, errorX, errorY)
    redrawAll(canvas)

def recordTime(canvas):
    elapsed=time.time()-canvas.data.time
    canvas.data.times.append(elapsed)    

def resetPath(canvas):
    canvas.data.trajectories.append(canvas.data.path)
    canvas.data.allPathTimes.append(canvas.data.pathTimes)
    canvas.data.path=[]
    canvas.data.pathTimes=[]
#    print canvas.data.trajectories

def motion(canvas, event): #store in a list and then delete lk hlaf
    if canvas.data.start: 
        x, y = event.x, event.y
        canvas.data.path.append((x,y))
        elapsed=time.time()-canvas.data.time
        canvas.data.pathTimes.append(elapsed)


def keyPressed(canvas, event):
    if (canvas.data.start==False and canvas.data.nameSet==True and event.keysym=="space"):
        canvas.data.start=True
        canvas.data.startScreen=False
        startClock(canvas)
        canvas.create_text(canvas.data.width/2, canvas.data.height/2, text=str(time.time()-canvas.data.time), font="Times 30")
    elif (canvas.data.start==False and canvas.data.nameSet==False):
        if event.keysym in string.ascii_letters:
            canvas.data.name=canvas.data.name+event.keysym
        elif event.keysym=="space":
            canvas.data.name=canvas.data.name+" "
        elif event.keysym=="BackSpace":
            canvas.data.name=canvas.data.name[:-1]
#            print canvas.data.name
        elif event.keysym=="Return":
            canvas.data.nameSet=True
    elif (canvas.data.start==True):
        canvas.data.keyPressed.append(canvas.data.clicks)
#        print (canvas.data.clicks, event.keysym) #see if a key was pressed
    redrawAll(canvas)

def startClock(canvas):
    canvas.data.time=time.time()

def timerFired(canvas):
    redrawAll(canvas)
    canvas.data.timerCounter += 1
    delay = 250 # milliseconds
    def f():
        timerFired(canvas) # DK: define local fn in closure
    canvas.after(delay, f) # pause, then call timerFired again


def redrawAll(canvas):   # DK: redrawAll() --> redrawAll(canvas)
    canvas.delete(ALL)
    if canvas.data.startScreen: #draw start screen
        drawStartScreen(canvas)
    else: #start circles
        if (canvas.data.start): #if started
            if canvas.data.clicks<canvas.data.numberToGo:  #while there's more circles to click
                drawCircles(canvas)
            else: #round finished 
                canvas.data.round+=1
                canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Section Completed", font="Times 30")
                canvas.create_text(canvas.data.width/2, canvas.data.height/2+100, text="Press the spacebar to start", font="Times 30")
                sectionFinished(canvas)
        else: #when inbetween rounds (so stopped )
            if canvas.data.round<canvas.data.numberOfRounds: #inbetween
                canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Section Completed", font="Times 30")
                canvas.create_text(canvas.data.width/2, canvas.data.height/2+100, text="Press the spacebar to start", font="Times 30")
            else: #final 
                canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Testing Complete", font="Times 30")

        #otherwize doesn't do anything (So in between the experiments)

def drawStartScreen(canvas):
    if canvas.data.nameSet==False:
        if canvas.data.timerCounter%4<2:
            canvas.create_text(canvas.data.width/2, canvas.data.height/2-100,text="Name:"+canvas.data.name,font="Times 30")
        else:
            canvas.create_text(canvas.data.width/2, canvas.data.height/2-100,text="Name:"+canvas.data.name+"_",font="Times 30")
    else: 
        canvas.create_text(canvas.data.width/2, canvas.data.height/2-100,text="Name:"+canvas.data.name,font="Times 30")

    canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Instructions:\n First, enter your name. Press enter when completed. \n Click the green circle", font="Times 30")
    canvas.create_text(canvas.data.width/2, canvas.data.height/2+100, text="Press the spacebar to start", font="Times 30")

def drawCircles(canvas):
    angle=(math.pi/2)-math.pi*(canvas.data.clicks)/25

    cX=(canvas.data.width/2)+(canvas.data.diameter/2)*math.cos(angle)*((-1)**canvas.data.clicks)
    cY=(canvas.data.height/2)-(canvas.data.diameter/2)*math.sin(angle)*((-1)**canvas.data.clicks)
    canvas.data.centerX=cX
    canvas.data.centerY=cY

    x1=cX-canvas.data.circleWidth/2
    y1=cY-canvas.data.circleWidth/2
    x2=cX+canvas.data.circleWidth/2
    y2=cY+canvas.data.circleWidth/2
    canvas.create_oval(x1,y1,x2,y2, fill="green")

def sectionFinished(canvas):
    writeFiles(canvas)
    writeTracking(canvas)
    readFile(canvas)
    setSecondaryValues(canvas)


##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


def writeFiles(canvas):
    savedTitle=str(canvas.data.name)+str(canvas.data.configuration)
    f=open(savedTitle, 'w')
#Find a way to organize data
    date = str(datetime.date.today())
    f.write(canvas.data.name+","+str(canvas.data.configuration)+","+date+"\n\n")
        #Header: subject name, configuration file used, date, 
    f.write("Target#, time, targetX, targetY, clicked, keyPressed, condition (W&D)\n")
        #write Body Header 
    for x in xrange(canvas.data.numberToGo):
        clicked=checkClicked(x, canvas)
        key=checkKeyPressed(x,canvas)
        stuff= str(x)+","+str(canvas.data.times[x])+","+\
            str(canvas.data.listcX[x])+","+str(canvas.data.listcY[x])+","+\
            clicked+","+key+","+str(canvas.data.circleWidth)+","+\
            str(canvas.data.diameter)+"\n"
        f.write(stuff)
        #Write body information

def checkClicked(x,canvas):
    for i in xrange(len(canvas.data.error)):
        if canvas.data.error[i]==x:
            return "1"
    return "0"

def checkKeyPressed(x, canvas):
    for i in xrange(len(canvas.data.keyPressed)):
        if canvas.data.keyPressed[i]==x:
            return "1"
    return "0"

def writeTracking(canvas):
    savedTitle=str(canvas.data.name)+str(canvas.data.configuration)+"tracking"
    f=open(savedTitle, 'w')
    date = str(datetime.date.today())
    f.write(canvas.data.name+","+str(canvas.data.configuration)+","+date+"\n")
    f.write("Target#, times, x, y \n")
    for x in xrange(canvas.data.numberToGo): #this x is wrt to clicks
        stuff=""
        timesForThisRound=canvas.data.allPathTimes[x] #1d list of [time1, time2, time3....]
        trajectory=canvas.data.trajectories[x] #1d list of (x,y)
#        print trajectory
#        print x
        for i in xrange(len(trajectory)):
            stuff=str(timesForThisRound[i]) #time 
            stuff=stuff+","+str(trajectory[i][0]) #x coordinate
            stuff=stuff+","+str(trajectory[i][1]) #y coordinate
            thing=str(x)+", "+str(stuff)+"\n"
            f.write(thing)

def openFile(canvas):
    root = Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
    canvas.data.condition=file_path
    #Set diameter and width to condition
    readFile(canvas)

def readFile(canvas):
    with open(canvas.data.condition) as f:
        for x in xrange(canvas.data.round+1):
            canvas.data.configuration=str(f.readline())
            if canvas.data.configuration=="":
                break
            f.readline()
            canvas.data.circleWidth=int(f.readline())
            f.readline()
            canvas.data.diameter=int(f.readline())

def init(canvas):

    canvas.data.diameter=30 #Filler in case of error
    canvas.data.circleWidth=10 #filler 

    canvas.data.round=0
    canvas.data.numberOfRounds=4


#################################################################################
#condition
    openFile(canvas)
#################################################################################
#set values
    setInitialValues(canvas) #doesn't change throughotu
    setSecondaryValues(canvas) #changes per round


def setInitialValues(canvas):
    canvas.data.name=""
    canvas.data.nameSet=False
    canvas.data.startScreen=True #Set to draw the starting screen


def setSecondaryValues(canvas): #for setting values 
##########################################################################################################
    canvas.data.times=[] #array of all the times it took to press the circle
    canvas.data.trajectories=[] #2d array of all paths
    canvas.data.path=[]  #1d array of a single path.
    canvas.data.pathTimes=[] 
    canvas.data.allPathTimes=[]
##############################################################################################################
    canvas.data.error=[]
    canvas.data.keyPressed=[]
    canvas.data.listcX=[]
    canvas.data.listcY=[]
 #########################################################################################################
    canvas.data.timerCounter = 0
 #########################################################################################################
    canvas.data.numberToGo=26 #number of clicks to do
    canvas.data.clicks=0
#########################################################################################################
    canvas.data.start=False #set not to start. Once enter is pressed starts.

def run():
    # create the root and the canvas
    root = Tk()
    cHeight=1150
    cWidth=1150
    canvas = Canvas(root, width=cWidth, height=cHeight)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=cWidth
    canvas.data.height=cHeight
    init(canvas) 
    root.bind("<Button-1>", lambda event:mousePressed(canvas,event))
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    root.bind("<Motion>", lambda event: motion(canvas, event))
    timerFired(canvas) 
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
run()



########### copy-paste below here ###########

#https://docs.python.org/2/tutorial/inputoutput.html
#http://stackoverflow.com/questions/6159900/correct-way-to-write-line-to-file-in-python
#http://www.mth.msu.edu/~jhall/classes/mth880-05/projects/latin.pdf #Latin Method



