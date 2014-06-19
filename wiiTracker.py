import os
import miniQueue as q
import pygame
from pygame.locals import *
import pickle
import os
import cwiid, time
from numpy import * #Import matrix libraries
from pylab import *
import funcs as fun
import time


class wiiTracker():
    def __init__(self):
        print "Press 1 & 2 on the Wiimote simultaneously to find it"
        try:
            self.wii = cwiid.Wiimote('00:23:CC:8F:AA:9E')
            self.wii.enable(cwiid.FLAG_MESG_IFC)
            self.wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
        except:
            print('Couldnt initialize the wiiMote')
    
    def capture(self):
        #Initialization of parameters
        X=0
        Y=0
        t=[]
        ir_x=[]
        ir_y=[]
        ir_s=[]
        rec_flg =0
        flg=True
        t_i = time.time()  
        running=False
        buff=[[],[]]
        maxBuff=120
        buff[0]=q.miniQueue(maxBuff)
        buff[1]=q.miniQueue(maxBuff)
        gestures=[[6,2,8,2,8],[9,3,9]]
        gestures=[ [str(i2) for i2 in i]for i in gestures]
        mouse_flg=0
        
        #Intialization of GUI
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        pygame.init()
        running=True
        pygame.display.set_mode((50,50), pygame.HWSURFACE)
        pygame.image.load("myimage.jpg").convert()
        print('press "r" to start recording')        
        
            
        while flg==True:
            #Capturing keyboard events first            
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    temp=chr(event.__dict__['key'])
                    print(temp)
                    if temp=='r':
                        rec_flg=1
                    elif temp=='s':
                        flg=False
                        break
                if event.type==QUIT:
                    flg=False
                    pygame.quit()

            #Capturing wii data                    
            messages = self.wii.get_mesg()        
            for mesg in messages:   
                #If message is IR data
                if mesg[0] == cwiid.MESG_IR: 
                    if rec_flg == 1:   
                        cont=-1
                        #loop through the IR sources
                        for s in mesg[1]:   
                            cont+=1
                            if s:   
                                print(s['pos'][0],s['pos'][1],cont)
                                ir_x.append(s['pos'][0])
                                ir_y.append(750-s['pos'][1])
                                ir_s.append(s['size'])
                                t.append(time.time()-t_i)    
#                                points[cont].append([s['pos'][0],s['pos'][1]])
                                buff[cont].put([s['pos'][0],s['pos'][1]])
                                if cont==0:
                                    X=1220-s['pos'][0]
                                    Y=s['pos'][1]
                                    
                    #Take out the false otherwise wont work
                    if buff[0].full() and buff[1].full() and False:
                        gest,cgest=fun.gestureReco(buff[0],buff[1],gestures)
                        gest=gest.strip('[]')
                        if gest!=None:
                            if gest==''.join(gestures[0]):
                                if mouse_flg==1:
                                    mouse_flg=0
                                    print('Mouse mode activated')
                                else:
                                    mouse_flg=1
                                    print('Mouse mode de-activated')
                                    
                            if gest==''.join(gestures[1]):
                                print('writing')
                            buff[0].erase()
                            buff[1].erase()
                            print(gest,cgest)
                            
                    if mouse_flg==1:
                        pygame.mouse.set_pos((X-360)*1366/500,(Y-150)*768/500)
                        print(X,Y)
                    

                            
                        

                elif mesg[0] == cwiid.MESG_BTN:  # If Message is Button data
                    if mesg[1] & cwiid.BTN_PLUS:    # Start Recording
                        rec_flg = 1
                        print "Recording..."
                    elif mesg[1] & cwiid.BTN_MINUS: # Stop Recording
                        flg=False
                        break
                
                if buff[0].size()>2 and buff[1].size()>2:                    
                    x0,y0=buff[0].data[-1]
                    x1,y1=buff[1].data[-1]
                    dist=np.sqrt((x0-x1)**2+(y0-y1)**2)
                    #print('%f,%f'%(dist,time.time()))
#                if self.key=='r' and rec_flg==0:
#                    rec_flg = 1
#                    print "Recording..."
                    
#                elif self.key=='s' and rec_flg==1:
#                    flg=False
#                    break
                    
        pygame.quit()
            


