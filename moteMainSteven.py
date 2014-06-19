from pymouse import PyMouse
from pykeyboard import PyKeyboard
import os
import miniQueue as q
import pygame
from pygame import mouse
from pygame.locals import *
import pickle
import os
import cwiid, time
from numpy import * #Import matrix libraries
from pylab import *
import funcs as fun
import time
import math
import copy
import copy


class mote():
    def __init__(self):
        print "Press 1 & 2 on the Wiimote simultaneously to find it"
        try:
            self.wii = cwiid.Wiimote('00:23:CC:8F:AA:9E')
            self.wii.enable(cwiid.FLAG_MESG_IFC)
            self.wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
        except:
            print('Couldnt initialize the wiiMote')

#Average Value Method
    def centerFind(self,rpt):
        xValue=0
        yValue=0
        for i in xrange(len(rpt)):
            xValue+=rpt[i][0]
            yValue+=rpt[i][1]
        xValue= xValue/len(rpt)
        yValue= yValue/len(rpt) 
        return xValue,yValue

    def findDegrees(self, rpt):
        orderList=[]
        cX,cY=self.centerFind(rpt)
        for i in xrange(len(rpt)):
            x,y=rpt[i][0],rpt[i][1]
            theta=self.arctan(cX,cY,x,y)
            theta-=45
            if theta<0:
                theta+=360
            orderList.append([theta,i])
            orderList.sort()
        return orderList

    def arctan(self, cX,cY,c,d):
        #a,b ar1e cx,cy locations
        delX=c-cX
        delY=d-cY
        theta=math.atan2( delX, delY)
        if theta<0:
            theta+=2*math.pi
        return theta*180/math.pi

    def indexData(self,newList):
        tipIndex=newList[1][1]
        tipIndexAngle=newList[1]
        kIndex=newList[0][1]
        kIndexAngle=newList[0][0]
        return tipIndex, tipIndexAngle, kIndex,kIndexAngle

    def thumbData(self,newList):
        tipThumb=newList[2][1]
        tipThumbAngle=newList[2][0]
        kThumb=newList[3][1]
        kThumbAngle=newList[3][0]
        return tipThumb,tipThumbAngle,kThumb,kThumbAngle

###############################################################################
    def rangeChecker(self,rptList,LED1, LED2,LED3,LED4):
        sameFlag=0
#append the new LED position
        LED1.append(rptList[len(rptList)-1][0])
        LED2.append(rptList[len(rptList)-1][1])
        LED3.append(rptList[len(rptList)-1][2])
        LED4.append(rptList[len(rptList)-1][3])
#check when LED is static
        sameFlag=self.outOfBounds(LED1,LED2,LED3,LED4)
        return (not (sameFlag)), LED1, LED2,LED3,LED4

#Doesnt Seem to be necessary
#check when LED is flickering
#        if not(sameFlag):
#            sameFlag=self.flickering(LED1,LED2,LED3,LED4)

    def outOfBounds(self, LED1,LED2,LED3,LED4):
        sameFlag=0
        if len(LED1)<10 or len(LED2)<10 or len(LED3)<10 or len(LED4)<10:
            pass
        else:
            flg1=self.checkEqual(LED1)
            flg2=self.checkEqual(LED2)
            flg3=self.checkEqual(LED3)
            flg4=self.checkEqual(LED4)
            if flg1 or flg2 or flg3 or flg4:
                sameFlag=1 #there is one thats same
            listOfLEDs=[LED1,LED2,LED3,LED4]
            for i in xrange(len(listOfLEDs)):
                thisLED=listOfLEDs[i]
                if (not (20<thisLED[len(thisLED)-1][0]<1180)) or (not (20<thisLED[len(thisLED)-1][1]<750)):
                    sameFlag=1
                    break
        return sameFlag

    def checkEqual(self, ledList):
        flg=0
        if (ledList[(len(ledList)-1)][0]==ledList[(len(ledList)-5)][0] and ledList[(len(ledList)-1)][1]==ledList[(len(ledList)-5)][1]):
            flg=1
        if flg:
            if (ledList[(len(ledList)-1)][0]==ledList[(len(ledList)-9)][0] and ledList[(len(ledList)-1)][1]==ledList[(len(ledList)-9)][1]):
                return flg
            else: 
                flg=0
                return flg
        return flg #its zero

    def flickering(self, LED1,LED2,LED3,LED4):
        flickeringFlag=0
        if len(LED1)<10 or len(LED2)<10 or len(LED3)<10 or len(LED4)<10:
            pass
        else:
            flg1=self.checkEqual(LED1)
            flg2=self.checkEqual(LED2)
            flg3=self.checkEqual(LED3)
            flg4=self.checkEqual(LED4)
            if flg1 or flg2 or flg3 or flg4:
                flickeringFlag=1 #there is one thats same
        return flickeringFlag

    def checkDifference(self, ledList):
        flg=0
        if ((abs(ledList[(len(ledList)-1)][0]-ledList[(len(ledList)-5)][0])>value) \
            or (abs(ledList[(len(ledList)-1)][1]-ledList[(len(ledList)-5)][1])>value)):
            flg=1
        return flg

    def allAboveGestureRight(self,rpt,gestureRightThreshHold):
        above=0
        for i in xrange(len(rpt)):
            if rpt[i][0]>=gestureRightThreshHold:
                above+=1
        return above/4
        
    def allAboveGestureLeft(self,rpt,gestureLeftThreshHold):
        above=0
        for i in xrange(len(rpt)):
            if rpt[i][0]<gestureLeftThreshHold:
                above+=1
        return above/4                   

    def allAboveGestureUp(self,rpt,gestureUpThreshHold):
        above=0
        for i in xrange(len(rpt)):
            if rpt[i][1]<gestureUpThreshHold:
                above+=1
        return above/4 

    def allAboveGestureDown(self,rpt,gestureDownThreshHold):
        above=0
        for i in xrange(len(rpt)):
            if rpt[i][1]>=gestureDownThreshHold:
                above+=1
        return above/4        
                  


    def capture(self):
#Initialization of parameters
        contDist=0
        inrange=0
        red = (255,0,0,120)
        green = (0,255,0)
        blue = (0,0,255)
        darkBlue = (0,0,128)
        white = (255,255,255)
        black = (0,0,0)
        yellow = (255,255,0)
        gray= (205,200, 177)
        rpt=[ [0,0] for i in range(4)]
        X=0
        Y=0
        t=[]
        ir_x=[]
        ir_y=[]
        ir_s=[]
        t_i = time.time()  
        m = PyMouse()
        k = PyKeyboard()
        running=False
        buff=[[],[]]
        maxBuff=20
        buff[0]=q.miniQueue(maxBuff)
        buff[1]=q.miniQueue(maxBuff)
        gestures=[[6,2,8,2,8],[9,3,9]]
        gestures=[ [str(i2) for i2 in i]for i in gestures]
#recording flags        
        rec_flg =0
        flg=True
        mouse_flg=0
        click_flg=0
        doubleClick_flg=0
        drag_flg=0
        dragX=0
        dragY=0
        wait_flg=0
        timeHold=80 #in milliseconds                

#calibration
        mouseModeValue=80
        clickValue=80
        lagValue=100
        calibration=False
        mouseModeCalib=False
        startMouseModeCalib=False
        clickingCalib=False
        startClickModeCalib=False
        mouseModeCalibList=[]
        clickingCalibList=[]
        rightClickValue=180
#Gesture
        gestureRightThreshHold=1000
        gestureLeftThreshHold=300
        gestureDownThreshHold=720
        gestureUpThreshHold=400
        gesture_flg_UD=0
        gesture_flg_DU=0
        gesture_flg_LR=0
        gesture_flg_RL=0
#Check inrange
        LED1=[]
        LED2=[]
        LED3=[]
        LED4=[]
        rptList=[]
#Intialization of GUI
        os.environ['SDL_VIDEO_iWINDOW_POS'] = "%d,%d" % (0,0)
        pygame.init()

        myfont=pygame.font.SysFont("monospace",15)
        calibFont=pygame.font.SysFont(",monospace",20)
        #the default cursor
        DEFAULT_CURSOR = mouse.get_cursor()  
        #the hand cursor
        _HAND_CURSOR = (
        "     XX         ",
        "    X..X        ",
        "    X..X        ",
        "    X..X        ",
        "    X..XXXXX    ",
        "    X..X..X.XX  ",
        " XX X..X..X.X.X ",
        "X..XX.........X ",
        "X...X.........X ",
        " X.....X.X.X..X ",
        "  X....X.X.X..X ",
        "  X....X.X.X.X  ",
        "   X...X.X.X.X  ",
        "    X.......X   ",
        "     X....X.X   ",
        "     XXXXX XX   ")
        _HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
        HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

        infoObject = pygame.display.Info()
        width=infoObject.current_w
        height=infoObject.current_h
        screen=pygame.display.set_mode((width/2,height/2))
        #screen=pygame.display.set_mode((1200/3,760/3))
        


        print('press "c" to calibrate, then')
        print('press "r" to start recording')        
        
        while flg==True:            

            if calibration: #do calibration
                newList=self.findDegrees(rpt) #[(theta1,i1),(theta2,i2)....)]
                tipIndex, tipIndexAngle, kIndex,kIndexAngle=self.indexData(newList)
                tipThumb,tipThumbAngle,kThumb,kThumbAngle=self.thumbData(newList)
                averageX,averageY=self.centerFind(rpt)
#GUI section
                screen.fill(black)
#Drawing the Circles
                pygame.draw.circle(screen, yellow, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
                pygame.draw.circle(screen, red, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
                pygame.draw.circle(screen, green, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
                pygame.draw.circle(screen, blue, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)
                pygame.draw.circle(screen, white, (averageX/3,averageY/3),10)

                mouseModeDistance=fun.distanceVec(\
                [rpt[tipIndex][0]],\
                [rpt[tipIndex][1]],\
                [rpt[tipThumb][0]],\
                [rpt[tipThumb][1]])

                clickingDistance=fun.distanceVec(\
                [rpt[kIndex][0]],\
                [rpt[kIndex][1]],\
                [rpt[tipThumb][0]],\
                [rpt[tipThumb][1]])

                pygame.draw.rect(screen, gray, (0,5,500,60))

                if not (mouseModeCalib or startClickModeCalib or startMouseModeCalib or clickingCalib):
                    Calib1=calibFont.render("Press H to start",1,black)
                    screen.blit(Calib1,(0,15))
                if startMouseModeCalib and not mouseModeCalib:
                    Calib1=calibFont.render("Tap tip of thumb and tip of index",1,black)
                    screen.blit(Calib1,(0,15))
                    Calib2=calibFont.render("Press H to complete",1,black)
                    screen.blit(Calib2,(0,35))
                    pygame.draw.line(screen,white,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),(rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),5 )
                    mouseModeCalibList.append(mouseModeDistance[0])                
                if startClickModeCalib and not clickingCalib:
                    Calib1=calibFont.render("Tap tip of thumb and knuckle of index",1,black)
                    screen.blit(Calib1,(0,15))
                    Calib2=calibFont.render("Press H to complete",1,black)
                    screen.blit(Calib2,(0,35))
                    pygame.draw.line(screen,white,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),(rpt[kIndex][0]/3,rpt[kIndex][1]/3),5 )
                    clickingCalibList.append(clickingDistance[0])                    
                if mouseModeCalib and clickingCalib:
                    calibrationDone=1
                    Calib1=calibFont.render("Calibration Completed",1,black)
                    screen.blit(Calib1,(0,15))
                    Calib2=calibFont.render("Press r to start recording",1,black)
                    screen.blit(Calib2,(0,35))
#Recording
            if rec_flg==1:
                newList=self.findDegrees(rpt) #[(theta1,i1),(theta2,i2)....)]
                tipIndex, tipIndexAngle, kIndex,kIndexAngle=self.indexData(newList)
                tipThumb,tipThumbAngle,kThumb,kThumbAngle=self.thumbData(newList)
                averageX,averageY=self.centerFind(rpt)
    #GUI section
                screen.fill(black)
    #Drawing the Circles
                pygame.draw.circle(screen, yellow, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
                pygame.draw.circle(screen, red, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
                pygame.draw.circle(screen, green, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
                pygame.draw.circle(screen, blue, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)
                pygame.draw.circle(screen, white, (averageX/3,averageY/3),10)
    #Drawing the Information Text
                ITLabel=myfont.render(  "IndexTip"+" "+str(tipIndexAngle),1,(25,255,255))
                screen.blit(ITLabel,(rpt[tipIndex][0]/3,rpt[tipIndex][1]/3))
                IKLabel=myfont.render(  "IndexKnuck"+" "+str(kIndexAngle)   ,1,(255,255,255))
                screen.blit(IKLabel,(rpt[kIndex][0]/3,rpt[kIndex][1]/3))
                TTLabel=myfont.render(  "ThumbTip"+" "+str(tipThumbAngle)   ,1,(255,255,255))
                screen.blit(TTLabel,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3))
                TKLabel=myfont.render(  "ThumbKnuck"+" "+str(kThumbAngle)   ,1,(255,255,255))
                screen.blit(TKLabel,(rpt[kThumb][0]/3,rpt[kThumb][1]/3))
                speedLabel=myfont.render("Increase:z, Decrease:x",1,(255,255,255))
                screen.blit(speedLabel,(0,65))
                mouseLabel=myfont.render("Mouse:"+" "+str(mouseModeValue) ,1,(255,255,255))
                screen.blit(mouseLabel,(0,80))
                clickLabel=myfont.render("Click:"+" "+str(clickValue) ,1,(255,255,255))
                screen.blit(clickLabel,(0,95))
    #Mouse Events
        #Drawing the mode
                if mouse_flg:
                    MouseKeyboard=myfont.render( "Mouse mode",1,(255,255,255))
                else:
                    MouseKeyboard=myfont.render( "Keyboard mode",1,(255,255,255))
                screen.blit(MouseKeyboard,(0,50))
        #Distance for switching modes
                dista=fun.distanceVec(\
                [rpt[tipIndex][0]],\
                [rpt[tipIndex][1]],\
                [rpt[tipThumb][0]],\
                [rpt[tipThumb][1]])
        #Distance for clicking - thumb tip to index knuckle
                distClick=fun.distanceVec(\
                [rpt[kIndex][0]],\
                [rpt[kIndex][1]],\
                [rpt[tipThumb][0]],\
                [rpt[tipThumb][1]])
    #Switching Modes
                if 10<=dista[0]<=mouseModeValue and inrange==1:                
                    contDist+=1                        
                if contDist>=timeHold and mouse_flg==0 and drag_flg==0:
                    print('Mouse mode activated')
                    mouse_flg=1
                    contDist=0
                    mouse.set_cursor(*HAND_CURSOR)
                if contDist>=timeHold and mouse_flg==1 and drag_flg==0:
                    print('Mouse mode deactivated')
                    mouse_flg=0
                    contDist=0
                    mouse.set_cursor(*DEFAULT_CURSOR)
        #Adjusting MaxBuff with respect to thumbtip and index knuckle
                if mouse_flg:
                    a=40*clickValue
                    maxBuff=a/distClick[0]
                    if maxBuff<20:
                        maxBuff=20
                    elif maxBuff>40:
                        maxBuff=40
    #Clicking
                if distClick[0]<clickValue and inrange and mouse_flg and not click_flg:
                    click_flg=1
                    stime=time.time()
                    m.click(buff[0].mean(),buff[1].mean())
                    dragX, dragY=buff[0].mean(),buff[1].mean()
                    print('Click')
                    print distClick[0]
                if (click_flg and (time.time()-stime)*1000>=lagValue and not drag_flg): #so its been 1/2 second, 
                    if (distClick[0]>=clickValue): #if finger is up, then delete flag. Else 
                        click_flg=0
                        drag_flg=0
                        print("reset")
                        print distClick[0]
                    elif ((dragX-buff[0].mean()>5) or (dragY-buff[1].mean()>5)): #Drag situation
                        m.press(dragX,dragY)
                        drag_flg=1
                        print ("dragging")
                        print distClick[0]
                if drag_flg and distClick[0]>=int(1.2*clickValue): #released the drag
                    drag_flg=0
                    m.release(buff[0].mean(),buff[1].mean())
                    dragX,dragY=0,0
                    print("release drag")
                    print distClick[0]
    #right click needs improvement #tried using the thumb
                #if mouse_flg and rightClick[0]>rightClickValue: 
                #    m.click(buff[0].mean(),buff[1].mean(),2)
    #Gestures
        #The gesture bounds
            #    pygame.draw.line(screen,white, (gestureRightThreshHold/3,0),(gestureRightThreshHold/3,800))
            #    pygame.draw.line(screen,red, (gestureLeftThreshHold/3,0),(gestureLeftThreshHold/3,800))
            #    pygame.draw.line(screen,blue, (0,gestureDownThreshHold/3),(10000,gestureDownThreshHold/3))
            #    pygame.draw.line(screen,yellow, (0,gestureUpThreshHold/3),(10000,gestureUpThreshHold/3))
        #Swipe Right to Left
                if self.allAboveGestureRight(rpt,gestureRightThreshHold) and not gesture_flg_RL:
                    gestureTime=time.time()
                    gesture_flg_RL=1
                    print("ready to gesture")
                if gesture_flg_RL and (time.time()-gestureTime)<1:
                    if self.allAboveGestureLeft(rpt, gestureLeftThreshHold):
                        k.press_key(k.control_key)
                        k.press_key(k.alt_key)
                        k.press_key(k.left_key)
                        k.release_key(k.control_key)
                        k.release_key(k.alt_key)
                        k.release_key(k.left_key)
                        gesture_flg_RL=0
        #Swipe Left to Right
                if self.allAboveGestureLeft(rpt,gestureLeftThreshHold) and not gesture_flg_LR:
                    gestureTime=time.time()
                    gesture_flg_LR=1
                    print("ready to gesture")
                if gesture_flg_LR and (time.time()-gestureTime)<1:
                    if self.allAboveGestureRight(rpt, gestureRightThreshHold):
                        k.press_key(k.control_key)
                        k.press_key(k.alt_key)
                        k.press_key(k.right_key)
                        k.release_key(k.control_key)
                        k.release_key(k.alt_key)
                        k.release_key(k.right_key)
                        gesture_flg_LR=0
        #Swipe Down to Up
                if self.allAboveGestureDown(rpt,gestureDownThreshHold) and not gesture_flg_DU:
                    gestureTime=time.time()
                    gesture_flg_DU=1
                    print("ready to gesture")
                if gesture_flg_DU and (time.time()-gestureTime)<1:
                    if self.allAboveGestureUp(rpt, gestureUpThreshHold):
                        k.press_key(k.control_key)
                        k.press_key(k.alt_key)
                        k.press_key(k.up_key)
                        k.release_key(k.control_key)
                        k.release_key(k.alt_key)
                        k.release_key(k.up_key)
                        gesture_flg_DU=0
        #Swipe Up to Down
                if self.allAboveGestureUp(rpt,gestureUpThreshHold) and not gesture_flg_UD:
                    gestureTime=time.time()
                    gesture_flg_UD=1
                    print("ready to gesture")
                if gesture_flg_UD and (time.time()-gestureTime)<1:
                    if self.allAboveGestureDown(rpt, gestureDownThreshHold):
                        k.press_key(k.control_key)
                        k.press_key(k.alt_key)
                        k.press_key(k.down_key)
                        k.release_key(k.control_key)
                        k.release_key(k.alt_key)
                        k.release_key(k.down_key)
                        gesture_flg_UD=0
                if gesture_flg_RL and (time.time()-gestureTime)>=1:
                    gesture_flg_RL=0
                if gesture_flg_LR and (time.time()-gestureTime)>=1:
                    gesture_flg_LR=0
                if gesture_flg_UD and (time.time()-gestureTime)>=1:
                    gesture_flg_UD=0
                if gesture_flg_DU and (time.time()-gestureTime)>=1:
                    gesture_flg_DU=0
    #Capturing keyboard events          
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==pygame.K_r: #start recording
                        rec_flg=1
                        calibration=False
                    elif event.key==pygame.K_c: #start calibration
                        calibration=1
                    elif event.key==pygame.K_s: #pauses the recording
                        rec_flg=False
                        break
                    elif event.key==pygame.K_q: #quits entirely
                        flg=False
                        break
                    if rec_flg: #if recording, can change the lag time
                        if event.key==pygame.K_z:
                            lagValue+=100
                        elif event.key==pygame.K_x:
                            lagValue-=100
                        

                #Mouse events for calibration mode
                    if calibration:
                        if not mouseModeCalib:
                            if not startMouseModeCalib and event.key==pygame.K_h:
                                startMouseModeCalib=True 
                            elif startMouseModeCalib and event.key==pygame.K_h:
                                mouseModeCalib=True
                                while min(mouseModeCalibList)<50:
                                    mouseModeCalibList.remove(min(mouseModeCalibList))
                                mouseModeValue=int(1.2*min(mouseModeCalibList))
                                mouseModeCalib=True
                        if mouseModeCalib:
                            if not startClickModeCalib and event.key==pygame.K_h:
                                startClickModeCalib=True
                            elif startClickModeCalib and event.key==pygame.K_h:
                                while min(clickingCalibList)<30:
                                    clickingCalibList.remove(min(clickingCalibList))
                                clickValue=int(1.2*min(clickingCalibList))
                                clickingCalib=True                            
                if event.type==QUIT:
                    flg=False
                    pygame.quit()
                    break
    #Capturing wii data                    
            messages = self.wii.get_mesg()    
            for mesg in messages:   # Loop through Wiimote Messages
                if mesg[0] == cwiid.MESG_IR: # If message is IR data
        #while recording data
                    if rec_flg == 1 or calibration:    # If recording
                        cont=-1
                        for s in mesg[1]:   # Loop through IR LED sources
                            cont+=1
                            if s:   # If a source exists
                                t.append(time.time()-t_i)
                                rpt[cont][0]=(1200-s['pos'][0])
                                rpt[cont][1]=s['pos'][1]
                    #Check inrange
                        newRpt=copy.deepcopy(rpt)
                        rptList.append(newRpt)
                        inrange, LED1,LED2,LED3,LED4=self.rangeChecker(rptList, LED1, LED2,LED3,LED4)
                #while in mouse mode
                    if mouse_flg==1:
                        X=rpt[tipIndex][0]
                        mouseX=(X-600)*width/400                    
                        Y=rpt[tipIndex][1]
                        mouseY=(Y-150)*height/290

                        """Currently we have the setting such that if there is a single LED that is out of range then
                        the mouse wont move. The problem with this is that the range of the mouse gets limited, and 
                        some places (such as corners) are difficult/impossible to click. If we eliminate the if statement
                        then this problem won't exist, but then it may start to recognize the knuckle LED as the tip and vice 
                        versa. So this is a give or take until we have a better filtering method."""

                        if inrange:
                            buff[0].put(mouseX)
                            buff[1].put(mouseY)
                            smoothX=np.mean(fun.smooth(buff[0].data, window_len=len(buff[0].data)))
                            smoothY=np.mean(fun.smooth(buff[1].data, window_len=len(buff[1].data)))
                            m.move(smoothX,smoothY)                    
                #I can also control using the wiimote
                elif mesg[0] == cwiid.MESG_BTN:  # If Message is Button data
                    if mesg[1] & cwiid.BTN_PLUS:    # Start Recording
                        rec_flg = 1
                        print "Recording..."
                    elif mesg[1] & cwiid.BTN_MINUS: # Stop Recording
                        flg=False
                        break
                pygame.display.update()         
        pygame.quit()
            


#when I tried to include double click as one
"""
if distClick[0]<clickValue and inrange and mouse_flg and not click_flg and not wait_flg and not doubleClick_flg:
    click_flg=1
    stime=time.time()
    m.click(buff[0].mean(),buff[1].mean())
    dragX, dragY=buff[0].mean(),buff[1].mean()
    print('Click')
    print click_flg,doubleClick_flg,drag_flg,wait_flg,mouse_flg
if ((click_flg and (time.time()-stime)*1000>=lagValue and not drag_flg) or (wait_flg)): #so its been 1/2 second, 
    if ((distClick[0]>=clickValue) or wait_flg): #if finger is up, then delete flag. Else 
        click_flg=0
        wait_flg=0
        drag_flg=0
        doubleClick_flg=0
        print "reset"
        print click_flg,doubleClick_flg,drag_flg,wait_flg,mouse_flg
    elif ((dragX-buff[0].mean()>5) or (dragY-buff[1].mean()>5)): #Drag situation
        m.press(dragX,dragY)
        drag_flg=1
        print ("dragging")
        print click_flg,doubleClick_flg,drag_flg,wait_flg,mouse_flg                        
if drag_flg and distClick[0]>=clickValue: #released the drag
    drag_flg=0
    m.release(buff[0].mean(),buff[1].mean())
    dragX,dragY=0,0
    print("release drag")
    print click_flg,doubleClick_flg,drag_flg,wait_flg,mouse_flg
#Double click. After once click, if above threshold, then give option of doubleClick
if distClick[0]>=clickValue and inrange and mouse_flg and click_flg:
    doubleClick_flg=1
if distClick[0]<clickValue and inrange and mouse_flg and click_flg and doubleClick_flg and not wait_flg:
    for i in xrange(2):
        m.click(buff[0].mean(),buff[1].mean())
    doubleClick_flg=0
    wait_flg=1
    click_flg=0
    print('Double Click')
    print click_flg,doubleClick_flg,drag_flg,wait_flg,mouse_flg
"""




#Awkward GUI for calibration
"""
if not mouseModeCalib and (startTime==0):
    startTime=time.time()
if not mouseModeCalib and (time.time()-startTime)<10:
    Calib1=calibFont.render("tap tip of index and thumb for"+" "+\
        str(int(10-(time.time()-startTime)))+"seconds",1,(255,255,255))
    screen.blit(Calib1,(0,65))
    mouseModeCalibList.append(mouseModeDistance[0])
if not mouseModeCalib and not((time.time()-startTime)<10):
    while min(mouseModeCalibList)<50:
        mouseModeCalibList.remove(min(mouseModeCalibList))
    mouseModeValue=int(1.2*min(mouseModeCalibList))
    mouseModeCalib=True
    startTime=0
    waitLabel=calibFont.render("wait",1,(255,255,255))
    screen.blit(waitLabel,(0,65))
    time.sleep(3)
if mouseModeCalib and not clickingCalib and startTime==0:
    startTime=time.time()
if mouseModeCalib and not clickingCalib and (time.time()-startTime)<10:
    Calib2=calibFont.render("tap tip of index and knuckle of thumb for"+" "+\
        str(int(10-(time.time()-startTime)))+"seconds",1,(255,255,255))
    screen.blit(Calib2,(0,65))                    
    clickingCalibList.append(clickingDistance[0])
if mouseModeCalib and not clickingCalib and not((time.time()-startTime)<10):    
    while min(clickingCalibList)<30:
        clickingCalibList.remove(min(clickingCalibList))
    clickValue=int(1.2*min(clickingCalibList))
    clickingCalib=True
if mouseModeCalib and clickingCalib:
    calibrationDone=1
    Calib3=calibFont.render("Press r to start recording",1,(255,255,255))
    screen.blit(Calib3,(0,65))
"""









