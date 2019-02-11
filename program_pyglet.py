# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:24:12 2019

@author: u262192
""" 
import os , sys, cv2, time, tkinter, PIL.Image, PIL.ImageTk
import multiprocessing, pyglet
from multiprocessing import Process, Manager
from os import listdir
# =============================================================================
# App
# =============================================================================
class App:
    def __init__(self, window, window_title, path):
        self.window = window
        self.path=path
        self.window.title(window_title)
        # open video source
        self.vid = MyVideoCapture()
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.anchor(anchor=tkinter.CENTER)
        self.canvas.pack()
    
        # Button that lets the user close and proceed
        self.btn_close=tkinter.Button(window, text="CLOSE", width=50, command=self.closee)
        self.btn_close.pack(anchor=tkinter.CENTER, expand=True)
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
        MediaLoad=pyglet.media.load(self.path+'\\vid\\music.wav')
        self.player.queue(MediaLoad)
        self.player.play()
             
    def closee(self):
        self.window.destroy()
        self.player.delete()

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
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)  
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# =============================================================================
# webcam
# =============================================================================

def webcam(global_list):
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        global_list.append([frame,time.time()])
    return()

# =============================================================================
# Funcitons
# =============================================================================
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
    
def closing_message():
    window = tkinter.Tk()
    window.title("Waiting")
    screen_w1=window.winfo_screenwidth()
    closing='\n'+'       Thank you for your participation in this experiment       \nThe app will now close itself in few secodns\n'
    tkinter.Label(window, text=closing,font=("Arial Bold", int(screen_w1/96)),anchor='center').pack()
    center(window)  #definition that takes in account everything and center the window
    window.mainloop()
    return()
    
###############################################################################
#                               MAIN                                          #
###############################################################################
if __name__ == '__main__':
    # multiprocess settings #
    multiprocessing.freeze_support()
    manager = Manager()
    shared_list = manager.list()
    
    # initial settings #
    log=list()
    final = find_folder() #find the folder where the script is in
    print('Detected folder path')
    log.append('Detected folder path'+' : '+str(time.time()))
    video0,video1,video2= findinpath(final+'\\vid') #selecting the videos in the folders
    print('Videos identified')
    log.append('Video identified'+' : '+str(time.time()))
    
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
    thank = tkinter.Label(window, text="\nThank you for participating to this experiment.\n",font=("Arial Bold", int(screen_w/80)),anchor='n').pack()
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
    App(tkinter.Tk(), "POSITIONING",final)  
    
    # =============================================================================
    # Last Chance
    # =============================================================================
    window = tkinter.Tk()
    window.title("Ready")  
    
    readyness='\n'+'       Pressing the START button will start the video       \n \n\
       If you need more time or you prefer to start the session later\n please click CLOSE and the program will shut-off   \n'
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
    task1 = Process(target=webcam, args=[shared_list])
    task1.start()
    print('Webcam activated')
    log.append('Webcam activated'+' : '+str(time.time()))
    time.sleep(3)
    # =============================================================================
    #  showing video
    # =============================================================================
    start, stop= (), ()
    start=time.time() #timestemp of start
    
    window=pyglet.window.Window(fullscreen=True)
    player=pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    MediaLoad=pyglet.media.load(showing)
    player.queue(MediaLoad)
    player.play()
    
    @window.event
    def on_draw():
        if player.source and player.source.video_format:
            player.get_texture().blit(0,0,width=screen_w, height=screen_h)       
    pyglet.app.run()
    
    '''closing video'''
    player.delete(), window.close(), player.delete(), source.delete()
    stop=time.time() #timestemp of stop
    pyglet.app.exit()
   
    log.append('Video start'+' : '+str(start))
    log.append('Video stop'+' : '+str(stop))
    '''terminate webcam'''
    task1.terminate()
    log.append('Webcam stoppped'+' : '+str(time.time()))
    '''append'''
    log.append('Video start'+' : '+str(start))
    log.append('Video stop'+' : '+str(stop))
    # =============================================================================
    # saving frames 
    # =============================================================================
    final_frames=[x for x in shared_list if start<=x[1]<=stop]
    fps= int(len(final_frames)/(final_frames[-1][1]-final_frames[0][1])) 
    fourcc = cv2.VideoWriter_fourcc(*"DIVX")#*'DIVX', *'mp4v', *'X264',  [mp4 +'avc1']
    out = cv2.VideoWriter(final+'\\data\\webcam_'+num+'.avi',fourcc,fps,(len(final_frames[0][0][1]),len(final_frames[0][0])))   
   
    time.sleep(3)
    # =============================================================================
    # message for waiting
    # =============================================================================
    task2 = Process(target=closing_message, args=[])
    task2.start() 

    print('Started saving frames')
    log.append('Started saving frames'+' : '+str(time.time()))
    for image in final_frames:
        out.write(image[0])
    out.release()
    
    print('Frames saved')
    log.append('Frames saved'+' : '+str(time.time()))
    logg= open(final+'\\data\\log_'+num+'.txt','w+')
    for err in log:
        logg.write(err+'\n') 
    logg.close() 
    print('BYBY and thank you again')
    task2.terminate()
    exit_all()
