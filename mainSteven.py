import threading
import time
import threadManSteven as tM
import Queue as q

buff=q.Queue(maxsize=20)


queueLock= threading.Lock()
print('starting thread')
#Last key pressedq
#This variable is going to be written by the gui threadb
#read by the mote threadg
#key=[]

#t1=tM.myThrelen(rpt)ad(0,'gui',buff,queueLock)
#t1.start()
t2=tM.myThread(1,'wii',buff,queueLock)
t2.start()  

#Change to the finger assignment using the angle instead of the current strategy

