# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:24:12 2019

@author: Tommaso Ghilardi
""" 
import os , sys, cv2, time, tkinter, PIL.Image, PIL.ImageTk
import pyglet
from os import listdir
from tkinter import ttk


# =============================================================================
# Waiting window + screen realted info
# =============================================================================
log=list() #logfile to store informations

window = tkinter.Tk()
screen_w,screen_h =window.winfo_screenwidth(),window.winfo_screenheight()# get width and height once for all

window.title("Waiting")
excuses='\n'+'      Welcome and thank you for participating in this study      '+'\n'
wating=tkinter.Label(window, text=excuses,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
window.attributes('-topmost', True) # note - before topmost
window.overrideredirect(True)
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
window.after(3000, lambda: window.destroy())
window.mainloop()

video_w, video_h=1440,1080
rapport = screen_h/video_h

# =============================================================================
# App for webcam feedback
# =============================================================================
class App:
    def __init__(self, window, window_title, path):
        self.window = window
        self.path=path
        self.window.title(window_title)
        # open video source
        self.vid = MyVideoCapture()
        if self.vid.width >= self.window.winfo_screenwidth() or self.window.winfo_screenheight() >= self.vid.height:
            w,h=self.vid.width/100*90, self.vid.height/100*90
        else:
            w,h=self.vid.width, self.vid.height
            
        self.canvas = tkinter.Canvas(window, width = w, height = h)
        self.canvas.anchor(anchor=tkinter.CENTER)
        self.canvas.pack()
    
        # Button that lets the user close and proceed
        self.btn_close=tkinter.Button(window, text="CLOSE", width=50, command=self.closee)
        self.btn_close.pack(expand=True)
        center(self.window)
        # Escape command that lets the user close
        self.window.bind("<Escape>",self.closee)
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.music()
        self.update()
        self.window.mainloop()
    
    def music(self):
        self.player=pyglet.media.Player()
        MediaLoad=pyglet.media.load(self.path+'\\vid\\music.mp3')
        self.player.queue(MediaLoad)
        self.player.play()
             
    def closee(self):
        self.window.destroy()
        self.player.delete()
        self.vid.closure()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image = self.photo, anchor = tkinter.NW)    
        else:
            self.window.destroy()
        self.window.after(self.delay, self.update)
                          
class MyVideoCapture:
    def __init__(self):
        # Open the video source
        self.vid = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source")

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.flip(frame,1)
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)  
    # Release the video source when the object is destroyed
    def closure(self):
        if self.vid.isOpened():
            self.vid.release()

# =============================================================================
# Funcitons
# =============================================================================
def find_folder():
    """find the path where the script is"""
    folder_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    log.append('Detected folder path'+' : '+str(time.time()))
    print('Detected folder path')
    return(folder_path)

def findinpath(pathh):
    """what video should be played"""   
    videos_check = 'video0.mp4', 'video1.mp4', 'video2.mp4','music.mp3'
    if set(videos_check)<= set(listdir(pathh)):
        Video0,Video1,Video2 =pathh+'\\'+'video0.mp4',pathh+'\\'+'video1.mp4',pathh+'\\'+'video2.mp4'
        print('Videos identified')
        log.append('Video identified'+' : '+str(time.time()))
    else:
        window = tkinter.Tk()
        window.title("Videos Problem")
        problem= '\n    The program is unable to detect the media files.    \n\n\
            If you have modified or moved a file to the USB stick, please restore the original state of the USB stick.    \n\
                If this is not possible, please contact the researcher following the provided instruction     \n\n'
        tkinter.Label(window, text=problem,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
        tkinter.Button(window, text="CLOSE the program",font=("Arial Bold",int(screen_w/96)), command=window.destroy, anchor='s').pack()
        center(window)  #definition that take in account everything and center the window
        window.mainloop()
        sys.exit()
    return(Video0,Video1,Video2)
        
def center(win):
    """centers a tkinter window"""
    win.overrideredirect(True)
    win.attributes('-topmost', True) # note - before topmost
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

def check_webcam():
    check = cv2.VideoCapture(0)
    if not check.isOpened():
        window = tkinter.Tk()
        window.title("Webcam Problem")
        problem= '    The program is unable to detect a webcam.    \n\
        Please make sure that your computer or device has access to a webcam and try to start the program again    \n\n'
        tkinter.Label(window, text=problem,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
        tkinter.Button(window, text="CLOSE the program",font=("Arial Bold",int(screen_w/96)), command=window.destroy, anchor='s').pack()
        center(window)  #definition that take in account everything and center the window
        window.mainloop()
        sys.exit()
    else:
        check.release()
        print('Webcam identified')
        log.append('Webcam identified'+' : '+str(time.time()))
        time.sleep(0.5)
    return()
        
def exit_all():
    sys.exit()
    window.destroy()

def evaluation_of_attention():
    options=0,0
    while sum(options)!=1:
        window = tkinter.Tk()
        request= "\n  Please evaluate the level of attention of the infant during this session on a scale  \n\
           from 0 to 10. Where 0 is extremely distracted and 10 is extremely attentive  \n"
        tkinter.Label(window, text=request,font=("Arial Bold",int(screen_w/96)),anchor='center').pack()
        lbl = tkinter.LabelFrame(window ,text="Steps:").pack()
        res1,res2,res3,res4,res5,res6,res7,res8,res9,res10 = tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar(),\
        tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar()
        
        c1 = tkinter.Checkbutton(lbl ,text="1" ,variable=res1, font=("Arial Bold", int(screen_w/96)))
        c2 = tkinter.Checkbutton(lbl ,text="2" ,variable=res2, font=("Arial Bold", int(screen_w/96)))
        c3 = tkinter.Checkbutton(lbl ,text="3" ,variable=res3, font=("Arial Bold", int(screen_w/96)))
        c4 = tkinter.Checkbutton(lbl ,text="4" ,variable=res4, font=("Arial Bold", int(screen_w/96)))
        c5 = tkinter.Checkbutton(lbl ,text="5" ,variable=res5, font=("Arial Bold", int(screen_w/96)))
        c6 = tkinter.Checkbutton(lbl ,text="6" ,variable=res6, font=("Arial Bold", int(screen_w/96)))
        c7 = tkinter.Checkbutton(lbl ,text="7" ,variable=res7, font=("Arial Bold", int(screen_w/96)))
        c8 = tkinter.Checkbutton(lbl ,text="8" ,variable=res8, font=("Arial Bold", int(screen_w/96)))
        c9 = tkinter.Checkbutton(lbl ,text="9" ,variable=res9, font=("Arial Bold", int(screen_w/96)))
        c10 = tkinter.Checkbutton(lbl ,text="10" ,variable=res10, font=("Arial Bold", int(screen_w/96)))
        
        c1.pack(),c2.pack(),c3.pack(),c4.pack(),c5.pack(),c6.pack(),c7.pack(),c8.pack(),c9.pack(),c10.pack(),
        tkinter.Button(window, text="CONTINUE",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack()
        center(window) 
        window.mainloop()
        options =[res1.get(),res2.get(),res3.get(),res4.get(),res5.get(),res6.get(),res7.get(),res8.get(),res9.get(),res10.get()]
    return(options.index(1) +1)
    
###############################################################################
#                               MAIN                                          #
###############################################################################    
final = find_folder() #find the folder where the script is in

video0,video1,video2= findinpath(final+'/vid') #selecting the videos in the folders

# =============================================================================
# check which video to show(which session we are)
# =============================================================================
if 'webcam_0.mp4' not in listdir(final+'\\data') and 'webcam_1.mp4' not in listdir(final+'\\data') and 'webcam_2.mp4' not in listdir(final+'\\data'):
    showing=video0
    num='0'
elif 'webcam_0.mp4' in listdir(final+'\\data') and 'webcam_1.mp4' not in listdir(final+'\\data') and 'webcam_2.mp4' not in listdir(final+'\\data'):
    showing=video1
    num='1'
elif 'webcam_0.mp4' in listdir(final+'\\data') and 'webcam_1.mp4' in listdir(final+'\\data') and 'webcam_2.mp4' not in listdir(final+'\\data'):
    showing=video2
    num='2'
else:
    window = tkinter.Tk()
    window.title("Already finished")
    thanks='\n'+'      It seems that you have already partecipated to all three sessions      \n\n \
          Thank for your time!!'+'\n'
    wating=tkinter.Label(window, text=thanks,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
    center(window)  #definition that take in account everything and center the window
    window.after(6000, lambda: window.destroy())
    window.mainloop()   
    sys.exit()

log.append('Identified session'+' : '+str(time.time()))
print('Identified session')

# =============================================================================
# Welcome window
# =============================================================================
window = tkinter.Tk()
window.title("Welcome")
thank = tkinter.Label(window, text="\nThank you for your participation to this experiment.\n",font=("Arial Bold", int(screen_w/80)),anchor='n').pack()
instructions= 'This study is divided in two phases: the training phase and the testing phase.\n\n \
The training phase will take place during the tree day before the test phase.\n \
During this period we ask you to show your sor or daughter tree videos (once every day) through this program.\n \
In each session a video will be displayed on your screen while a feedback from the webcam will be recorded.\n\n\
The program will not install anything on your device and the videos will be only saved on the USb drive:\n\
you will have total controll over them\n\n\
    The videos will be analyzed in order to evaluate how much the stimuli were able to capture the attention of the child.    \n\n \
When ready, click on the CONTINUE button to progress in the session\n'

instruction=tkinter.Label(window, text=instructions,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
btn = tkinter.Button(window, text="CONTINUE",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack()
center(window)  #definition that take in account everything and center the window
window.mainloop()

'''checking the webcam'''
check_webcam()

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
App(tkinter.Tk(), "POSITIONING",final) 
print('Image checked on webcam')
log.append('Image checked on webcam'+' : '+str(time.time())) 

# =============================================================================
# Last Chance
# =============================================================================
window = tkinter.Tk()
window.title("Ready")  

readyness='\n'+'       Pressing the START button will start the video session       \n\
       The session will last around 9 minutes.       \n \n\
   If you need more time or you prefer to start the session later\n please click CLOSE and the program will shut-off   \n\n\
   If you decide to proceed please click START and try to show\n the entire session to your son or daughter. \
If for any reason you\n will decide to interruprt the session please press the ESC key\n'
ready=tkinter.Label(window, text=readyness,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
window.update_idletasks()
btn = tkinter.Button(window, text="START",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack(side=tkinter.LEFT,padx=window.winfo_width()/5,pady=window.winfo_height()/8.3)
close_btn= tkinter.Button(window, text="CLOSE",font=("Arial Bold", int(screen_w/96)), command=exit_all, anchor='s').pack(side=tkinter.RIGHT,padx=window.winfo_width()/5,pady=window.winfo_height()/8.3)
center(window)  #definition that takes in account everything and center the window
window.mainloop()
print('Session accepted')
log.append('Session accepted'+' : '+str(time.time()))

# =============================================================================
# webcam activation
# =============================================================================
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
print('Webcam activated')
log.append('Webcam activated'+' : '+str(time.time()))

frames = list()
time.sleep(1)

# =============================================================================
#  showing video
# =============================================================================
window=pyglet.window.Window(fullscreen=True)
player=pyglet.media.Player()
source = pyglet.media.StreamingSource()
MediaLoad=pyglet.media.load(showing)
player.queue(MediaLoad)
player.play()
start=time.time() #timestemp of start

@window.event
def on_draw():
    if player.source and player.source.video_format:
        player.get_texture().blit(screen_w/2-video_w*rapport/2, screen_h/2-video_h*rapport/2 , width=video_w*rapport, height=video_h*rapport)
        ret, frame = cap.read()
        frames.append([frame,time.time()])

pyglet.app.run()
stop=time.time() #timestemp of stop

'''closing video'''
#player.delete(),
window.close(), player.delete(), source.delete()
pyglet.app.exit()
cap.release()
log.append('Webcam stoppped'+' : '+str(stop))

log.append('Video start'+' : '+str(start))
log.append('Video stop'+' : '+str(stop))
print('part1')

# =============================================================================
# Selection frames
# =============================================================================
'''extracting framerate'''
raw_fps = len(frames)/(frames[-1][1]-frames[0][1])
fps= int(raw_fps)
log.append('Video palyed at'+' : '+str(fps))
print(raw_fps)

'''settign saving'''
fourcc = cv2.VideoWriter_fourcc(*"mp4v")#*'DIVX', *'mp4v', *'X264',  [mp4 +'avc1'] [avi + 'DIVX']
out = cv2.VideoWriter(final+'/data/webcam_'+num+'.mp4',fourcc,fps,(len(frames[0][0][1]),len(frames[0][0])))      
time.sleep(1)

## =============================================================================
## Saving frames
## =============================================================================
'''message of waiting'''
window = tkinter.Tk()
window.title('Saving')
progress_var = tkinter.DoubleVar() #here you have ints but when calc. %'s usually floats
saving='\n    The video session is finished.    \n\
    Please wait few seconds while the program saves the webcam video.    \n\
    Please do not turn off the computer and do not eject the USB drive    \n'
tkinter.Label(window, text=saving,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
progressbar = ttk.Progressbar(window, variable=progress_var, maximum=100)
progressbar.pack(fill=tkinter.X, expand=1, pady=int(screen_w/54))
center(window)

print('Started saving frames')
log.append('Started saving frames'+' : '+str(time.time()))

for images in range(0,len(frames)):
    image= frames[images]
    out.write(frames[images][0])
    percentage= 100*images/len(frames)
    apporx = int(percentage/5)*5
    
    progress_var.set(apporx)
    window.update()
time.sleep(3)  # just to have  smoother transition
window.destroy()
out.release()
log.append('Frames saved'+' : '+str(time.time()))
print('Frames saved')

time.sleep(1)
# =============================================================================
# asking evaluation
# =============================================================================
answer=evaluation_of_attention()
log = ['The level of attention was rated as : '+ str(answer)+'\n\n'] +log  #the evalution of attention of the infant
log = ['Video presented on '+ time.ctime()+ '\n']+ log  #saving the day and the time the video was shown

# =============================================================================
# saving logs
# =============================================================================
logg= open(final+'\\data\\log_'+num+'.txt','w+')
for err in log:
    logg.write(err+'\n') 
logg.close() 

# =============================================================================
# BYBY
# =============================================================================
window = tkinter.Tk()
window.title("Goodbye")
byby= '\n    The experiment is now finished.    \n\n    Thank you for your participation    \n'

tkinter.Label(window, text=byby,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
btn = tkinter.Button(window, text="BYBY",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack()
center(window)  #definition that take in account everything and center the window
window.mainloop()
sys.exit()