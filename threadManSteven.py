import moteMainSteven
import Queue
import threading
import time
import gui
global exitFlag
exitFlag=0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q, qL):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.qL=qL

        
    def run(self):
        print "Starting " + self.name
        if self.name=='gui':
            app=gui.App()
            app.on_execute()
        elif self.name=='wii':      
            wii=moteMainSteven.mote()           
            wii.capture()
            

        print "Exiting " + self.name

def process_data(threadName, q,qL):
    while not exitFlag:
        qL.acquire()
        if not q.empty():
            data = q.get()
            qL.release()
            print "%s processing %s\n" % (threadName, data)
        else:
            qL.release()

