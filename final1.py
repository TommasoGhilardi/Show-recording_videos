# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 09:18:43 2019

@author: u262192
"""
###############################################################################
#                                                                             #
#                               Lybraries                                     #
#                                                                             #
###############################################################################
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import os,sys
from os import listdir

log=list()
frame_recording=list()
time_recording=list()
width_web=list()
height_web=list()
###############################################################################
#                               Apps                                          #
###############################################################################
class App:
    def __init__(self, window, window_title, video_source,pathh,numm):
        self.window, self.pathh, self.numm= window, pathh, numm
        self.window.title(window_title)
        self.delay = 10
        
        
        if video_source == 0 + cv2.CAP_DSHOW:
            self.TYPE=1
            # open video source
            self.vid = MyVideoCapture(video_source,self.TYPE)
            self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
            self.window.attributes("-topmost", True)
            self.canvas.pack()
        
            # Button that lets the user take a snapshot
            self.btn_snapshot=tkinter.Button(window, text="CLOSE", width=50, command=self.closee)
            self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
            print('Webcam positioning')
            log.append('Webcam positioning'+' : '+str(time.time()))
            
            # Escape command that lets the user close
            self.window.bind("<Escape>",self.closee) 
            # After it is called once, the update method will be automatically called every delay milliseconds
            self.update1()
            self.window.mainloop()
            
        else:   
            self.TYPE=2
            # open video source
            self.vid = MyVideoCapture(video_source, self.TYPE)
            # Create a canvas that can fit the above video source size
            self.canvas = tkinter.Canvas(window, width = screen_w, height = screen_h, bg="black",highlightthickness=0)
            self.window.attributes("-fullscreen",True)
            self.window.attributes("-topmost", True)
            self.canvas.pack()
            print('Showing video')
            log.append('Showing video'+' : '+str(time.time()))
        
            # Escape command that lets the user close
            self.window.bind("<Escape>",self.closee) 
            # After it is called once, the update method will be automatically called every delay milliseconds
            
            self.update2()
            self.window.mainloop()
        
    def closee(self,event=None):
        self.window.destroy()

    def update1(self):
        # Get a frame from the webcam for trial
        ret, frame = self.vid.get_frame1()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image = self.photo, anchor = tkinter.NW)                
        self.window.after(self.delay, self.update1)
            
    def update2(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame2()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(screen_w/2-self.vid.width/2, screen_h/2-self.vid.height/2, image = self.photo, anchor = tkinter.NW)
        else:
            print('Video finished')
            log.append('Video finished'+' : '+str(time.time()))
            self.window.destroy()
        self.window.after(self.delay, self.update2)
            
       
class MyVideoCapture:
    def __init__(self, video_source,TYPE):
        self.TYPE=TYPE
        #webcam if  needed
        if self.TYPE==2:
            self.webcam=cv2.VideoCapture(0 + cv2.CAP_DSHOW)
            if not self.webcam.isOpened():
                raise ValueError("Unable to open webcam")
            width_web.append(self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
            height_web.append(self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            time.sleep(1)
            
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
               
    def get_frame1(self):
        #only webcam frame
        ret, frame = self.vid.read()
        if ret:
            # Return a boolean success flag and the current frame converted to BGR
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return (ret, None)

    def get_frame2(self):
        #video while saving webcam frames
        ret, frame = self.vid.read()
        ret_web, frame_web= self.webcam.read()
        if ret:
            frame_recording.append(frame_web)
            time_recording.append(time.time())
            # Return a boolean success flag and the current frame converted to BGR
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return (ret, None) 

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.TYPE==2:
            if self.vid.isOpened():
                self.vid.release()
            if self.webcam.isOpened():
                self.webcam.release()         
        else:
            if self.vid.isOpened():
                self.vid.release()
            
###############################################################################
#                            Functions                                        #
###############################################################################
def find_folder():
    """find the path where the script is"""
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def findinpath(pathh):
    """what video should be played"""
    for x in listdir(pathh):
        if 'video0' in x:
            Video0=pathh+'\\'+x
        elif 'video1' in x:
            Video1= pathh+'\\'+x
        elif 'video2' in x:
            Video2=pathh+'\\'+x
    return(Video0,Video1,Video2)      

def center(win):
    """centers a tkinter window"""
    win.overrideredirect(True)
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    return()

def exit_all():
    exit()
    window.destroy()       
###############################################################################
#                               MAIN                                          #
###############################################################################
  
# =============================================================================
# find folder path + videos
# =============================================================================
final = find_folder()
print('Detected folder path')
log.append('Detected folder path'+' : '+str(time.time()))

video0,video1,video2= findinpath(final+'\\vid')
print('Video selected')
log.append('Video selected'+' : '+str(time.time()))

# =============================================================================
# Waiting window
# =============================================================================
window = tkinter.Tk()
window.title("Waiting")

screen_w,screen_h =window.winfo_screenwidth(),window.winfo_screenheight()# get width and height once for all

excuses='\n'+'      Welcome and thank you for participating in this study      '+'\n'

wating=tkinter.Label(window, text=excuses,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
center(window)  #definition that take in account everything and center the window
window.after(3000, lambda: window.destroy())
window.mainloop()

# =============================================================================
# check which video to show(which session we are)
# =============================================================================
if 'webcam_0.mp4' not in listdir(final+'\\data'):
    showing=video0
    num='0'
elif 'webcam_0.mp4' in listdir(final+'\\data') and 'webcam_1.avi' not in listdir(final+'\data'):
    showing=video1
    num='1'
elif 'webcam_0.mp4' in listdir(final+'\\data') and 'webcam_1.avi' in listdir(final+'\data'):
    showing=video2
    num='2'
    
# =============================================================================
# Welcome window
# =============================================================================
window = tkinter.Tk()
window.title("Welcome")

thank = tkinter.Label(window, text="Thank you for participating to this experiment.\n",font=("Arial Bold", int(screen_w/80)),anchor='n').pack()

instructions= 'This study is divided in two phases: the training phase and the testing phase.\n\n \
The training phase will take place during the tree day before the test phase. During this period we \n \
ask you to show your child tree videos (once every day) through this program.\n \
    During each of these training session a video will be displayed on your screen while we will record a feedback from the webcam.    \n \
The videos will be analyzed in order to evaluate how much the stimuli were able to capture the attention of the child.\n \
On the fourth day we ask you to come to Radboud University Labs for the testing phase.\n\n \
When ready, click on the CONTINUE button to progress in the sessionn\n\n \
If for any reason you will decide to interruprt the recording please press the ESC key.\n'

instruction=tkinter.Label(window, text=instructions,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
btn = tkinter.Button(window, text="CONTINUE",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack()
center(window)  #definition that take in account everything and center the window
window.mainloop()

# =============================================================================
# Ready window
# =============================================================================
window = tkinter.Tk()
window.title("Ready") 
 
position='\n    Pressing the TRIAL button you will see a video feedback from your webcam.    \n \
Try to position your child in front of the webcam in order\n to have the best view possible of his/her gaze\n '
ready=tkinter.Label(window, text=position,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()

btn = tkinter.Button(window, text="TRIAL",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack()
center(window)  #definition that take in account everything and center the window
window.mainloop()

# =============================================================================
# Feedback webcam position
# =============================================================================
App(tkinter.Tk(), "Tkinter and OpenCV", 0 + cv2.CAP_DSHOW,'no','no')

# =============================================================================
# Last Chance
# =============================================================================
window = tkinter.Tk()
window.title("Ready")  
screen_w,screen_h =window.winfo_screenwidth(),window.winfo_screenheight()# get width and height once for all

readyness='\n'+'       Pressing the START button will start the video       \n \n\
   If you need more time or you prefer to start the session later\n please click CLOSE and the program will shut-off   \n'
ready=tkinter.Label(window, text=readyness,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
center(window)  #definition that take in account everything and center the window
window.update_idletasks()

btn = tkinter.Button(window, text="START",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack(side=tkinter.LEFT,padx=window.winfo_width()/5,pady=window.winfo_height()/8.3)
close_btn= tkinter.Button(window, text="CLOSE",font=("Arial Bold", int(screen_w/96)), command=exit_all, anchor='s').pack(side=tkinter.RIGHT,padx=window.winfo_width()/5,pady=window.winfo_height()/8.3)
window.mainloop()

# =============================================================================
# Show video
# =============================================================================
App(tkinter.Tk(), "Tkinter and OpenCV", showing, final, num)

# =============================================================================
# beginning of the closing procedure
# =============================================================================
print('Closing procedure')
log.append('Closing procedure'+' : '+str(time.time()))
fps= int(len(frame_recording)/(time_recording[-1]-time_recording[0]))
fourcc = cv2.VideoWriter_fourcc(*"DIVX")#*'DIVX', *'mp4v', *'X264',  [mp4 +'avc1']
out = cv2.VideoWriter(final+'\\data\\webcam_'+num+'.avi',fourcc,fps,(int(width_web[0]),int(height_web[0])))

# =============================================================================
# message for waiting
# =============================================================================
window = tkinter.Tk()
window.title("Waiting")
screen_w1=window.winfo_screenwidth()
    
closing='\n'+'       Thank you for your participation in this experiment       \nThe app will now close itself in few secodns\n'

tkinter.Label(window, text=closing,font=("Arial Bold", int(screen_w1/96)),anchor='center').pack()
center(window)  #definition that take in account everything and center the window
window.after(4000, lambda: window.destroy())
window.mainloop()

# =============================================================================
# write the frame to file mp4
# =============================================================================
print('Saving precise frames')
log.append('Saving precise frames'+' : '+str(time.time()))

for image in frame_recording:
    out.write(image)
out.release()

print('Frames saved')
log.append('Frames saved'+' : '+str(time.time()))
logg= open(final+'\\data\\log_'+num+'.txt','w+')
for err in log:
    logg.write(err+'\n') 
logg.close() 
print('BYBY and thank you again')