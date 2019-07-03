# -- coding: utf-8 --
"""
Created on Thu Feb  7 14:24:12 2019

@author: Tommaso Ghilardi
""" 
import os , sys, cv2, time, tkinter, PIL.Image, PIL.ImageTk
import pyglet, multiprocessing
from os import listdir

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
        
        # Positioning
        self.window.update_idletasks()
        self.window.overrideredirect(True)
        self.width= self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.x= (self.window.winfo_screenwidth()//2)-(self.width/2)
        self.y= 0
        self.window.geometry('%dx%d+%d+%d' % (self.width,self.height,self.x,self.y))
        self.window.attributes('-topmost', True)
        # Escape command that lets the user close
        self.window.bind("<Escape>",self.closee)
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        self.window.mainloop()
             
    def closee(self):
        self.window.destroy()
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
        self.vid = cv2.VideoCapture(0)
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
    videos_check = 'video0.mp4', 'video1.mp4', 'video2.mp4'
    if set(videos_check)<= set(listdir(pathh)):
        Video0,Video1,Video2 =pathh+'/'+'video0.mp4',pathh+'/'+'video1.mp4',pathh+'/'+'video2.mp4'
        print('Videos identified')
        log.append('Video identified'+' : '+str(time.time()))
    else:
        window = tkinter.Tk()
        window.title("Videos Problem")
        problem= '\nThe program is unable to detect the media files.\n\n\
           If you have modified or moved any file on the USB drive, please restore the original state of the USB drive.   \n\
        If unable to restore the original state, please contact the researcher by following the provided instruction.\n\n'
        tkinter.Label(window, text=problem,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
        tkinter.Button(window, text="CLOSE the program",font=("Arial Bold",int(screen_w/96)), command=window.destroy, anchor='s').pack()
        center(window)  #definition that take in account everything and center the window
        window.mainloop()
        sys.exit()
    return(Video0,Video1,Video2)
        
def center(win):
    win.update_idletasks()
    win.overrideredirect(True)
    width= win.winfo_width()
    height = win.winfo_height()
    x= (win.winfo_screenwidth()//2)-(width/2)
    y= (win.winfo_screenheight()//2)-(height/2)
    win.geometry('%dx%d+%d+%d' % (width,height,x,y))
    win.attributes('-topmost', True)
#    win.deiconify()
    return()

def check_webcam(manager_of_frames):
    fps_testing=0
    check = cv2.VideoCapture(0)

    if check.isOpened():
        start_testing=time.time()
        while fps_testing<240:
            ret, frame = check.read()
            frame=cv2.resize(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),(320,240),interpolation=cv2.INTER_NEAREST)
            fps_testing= fps_testing+1
        stop_testing=time.time()
        manager_of_frames.value=round(fps_testing/(stop_testing-start_testing))
        print(str(manager_of_frames.value))
        check.release()
        print('Webcam identified')
        
    elif not check.isOpened():
        manager_of_frames.value=2
    return()

def webcam(stopper,fps,path,numm):
    print(str(fps.value))
    cap = cv2.VideoCapture(0)
    width_w= 320
    height_w= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*width_w/cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")#'DIVX', *'mp4v', *'X264',  [mp4 +'avc1'] [avi + 'DIVX']
    out = cv2.VideoWriter(path+'/data/webcam_'+numm+'.mp4',fourcc,fps.value,(width_w,height_w),isColor=False)
    out.set(cv2.VIDEOWRITER_PROP_QUALITY,1)
    
    while True:
        if stopper.value==1:
            ret, frame = cap.read()
            frame=cv2.resize(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),(width_w,height_w),interpolation=cv2.INTER_NEAREST)
            if ret==True:
                out.write(frame)
        elif stopper.value==0:
            continue
        elif stopper.value==2:    
            cap.release()
            break
    return()
      
def exit_all():
    sys.exit()
    window.destroy()
    

if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    '''pyglet check'''
    pyglet.lib.load_library('avbin')    
    pyglet.have_avbin=True
       
    # =============================================================================
    # Waiting window + screen realted info
    # =============================================================================
    log=list() #logfile to store informations
    
    window = tkinter.Tk()
    screen_w,screen_h =window.winfo_screenwidth(),window.winfo_screenheight()# get width and height once for all
    window.title("Waiting")
    excuses='\n'+'      Welcome and thank you for participating in this study      '+'\n'
    wating=tkinter.Label(window, text=excuses,font=("Arial Bold", int(screen_w/96))).pack()
    window.after(3000, lambda: window.destroy())
    
    window.update_idletasks()
    window.overrideredirect(True)
    width= window.winfo_width()
    height = window.winfo_height()
    x= (window.winfo_screenwidth()//2)-(width/2)
    y= (window.winfo_screenheight()//2)-(height/2)
    window.geometry('%dx%d+%d+%d' % (width,height,x,y))
    window.attributes('-topmost', True)
    window.mainloop()
    
    # Get time and date
    log.append('Video watched on'+' : '+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    
    video_w, video_h=1440,1080
    rapport = screen_h/video_h   
    
    # =============================================================================
    #  Main   
    # =============================================================================
    final = find_folder() #find the folder where the script is in
    SET = [s for s in listdir(final) if 'set' in s][0]
    log.insert(0,'The training set is: '+SET+'\n')
    video0,video1,video2= findinpath(final+'/'+SET)  #selecting the videos in the folders

    # =============================================================================
    # check which video to show(which session we are)
    # =============================================================================
    if 'webcam_0.mp4' not in listdir(final+'/data') and 'webcam_1.mp4' not in listdir(final+'/data') and 'webcam_2.mp4' not in listdir(final+'/data'):
        showing=video0
        num='0'
    elif 'webcam_0.mp4' in listdir(final+'/data') and 'webcam_1.mp4' not in listdir(final+'/data') and 'webcam_2.mp4' not in listdir(final+'/data'):
        showing=video1
        num='1'
    elif 'webcam_0.mp4' in listdir(final+'/data') and 'webcam_1.mp4' in listdir(final+'/data') and 'webcam_2.mp4' not in listdir(final+'/data'):
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
    # Multiprocessing setting
    # =============================================================================
    fps_manager = manager.Value('i', 0)
    stopper_manager = manager.Value('i',0)
    
    process1 = multiprocessing.Process(target=check_webcam, args=(fps_manager,)) 
    process2 = multiprocessing.Process(target=webcam, args=(stopper_manager,fps_manager,final,num)) 
    
    # =============================================================================
    # Welcome window
    # =============================================================================
    process1.start()
        
    window = tkinter.Tk()
    window.title("Welcome")
    thank = tkinter.Label(window, text='\nThank you for participating in this study.\n',font=("Arial Bold", int(screen_w/80)),anchor='n').pack()
    instructions='This study is divided into two phases: the training phase and the testing phase.\n\n \
    The training phase will take place during the three days before the test phase.\n \
    During this period we ask you to watch three videos (one each day) using this program.\n \
    In each session a video will be displayed on your screen, while a feedback from the webcam will be recorded.\n\n\
       The program will not install anything on your device and the videos will only be saved on the encrypted USB drive:   \n\
    you will have complete control over them.\n\n\
    Please remember to bring the USB drive to the test phase.\n\
    The videos will be analyzed in order to evaluate the level of attention paid to the stimuli.\n\n \
    When you are ready, click on the CONTINUE button to progress with the session.\n'
    
    instruction=tkinter.Label(window, text=instructions,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
    btn = tkinter.Button(window, text="CONTINUE",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack()
    center(window)  #definition that take in account everything and center the window
    window.mainloop()
    
    '''checking the webcam'''
    process1.join()
    # =============================================================================
    # Problem webcam
    # =============================================================================
    if fps_manager.value==2:
        window = tkinter.Tk()
        window.title("Webcam Problem")
        problem= '\n    The program is unable to detect a webcam.    \n\
        Please make sure that your computer or device has access to a webcam and try to start the program again    \n\n'
        tkinter.Label(window, text=problem,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
        tkinter.Button(window, text="CLOSE the program",font=("Arial Bold",int(screen_w/96)), command=window.destroy, anchor='s').pack()
        center(window)  #definition that take in account everything and center the window
        window.mainloop()
        sys.exit()
 
    log.append('Webcam identification'+' : '+str(time.time())) 
    log.append('Framerate of'+' : '+str(fps_manager.value)+' fps')
        
    # =============================================================================
    # Ready window
    # =============================================================================
    window = tkinter.Tk()
    window.title("Ready") 
    position='\n   Pressing the TRIAL button will display a video feedback from your webcam.   \n \
    Try to position yourself in front of the webcam in order\n to frame your face as accurately as possible. \n'
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
    
    readyness='\nPressing the START button will start the video session.\n\
    The session will last around 12 minutes.\n\n\
    If you are not ready or you prefer to start the session later,\n please click CLOSE and the program will close.\n\n\
       If you decide to proceed please click the START button. We ask you to try to watch the entire session.   \n\n\
    If for any reason you decide to interrupt the session please press the ESC key.\n'
    ready=tkinter.Label(window, text=readyness,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
    window.update_idletasks()
    btn = tkinter.Button(window, text="START",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack(side=tkinter.LEFT,padx=window.winfo_width()/5,pady=window.winfo_height()/8.3)
    close_btn= tkinter.Button(window, text="CLOSE",font=("Arial Bold", int(screen_w/96)), command=exit_all, anchor='s').pack(side=tkinter.RIGHT,padx=window.winfo_width()/5,pady=window.winfo_height()/8.3)
    center(window)  #definition that takes in account everything and center the window
    window.mainloop()
    print('Session accepted')
    log.append('Session accepted'+' : '+str(time.time()))

    # =============================================================================
    #  showing video
    # =============================================================================
    process2.start()
    print('Webcam activated')
    log.append('Webcam activated'+' : '+str(time.time()))
        
    pos1,pos2,dim1,dim2=screen_w/2-video_w*rapport/2, screen_h/2-video_h*rapport/2 ,video_w*rapport,video_h*rapport
    window=pyglet.window.Window(fullscreen=True, vsync= True)
    player=pyglet.media.Player()
    source = pyglet.media.load(showing)
    source.video_format.frame_rate=30
    stopper= source.duration-1
    player.queue(source)
    player.play()
    stopper_manager.value=1
    start=time.time() #timestemp of start
    
    @window.event
    def on_draw():
        window.clear()
        if player.source and player.source.video_format:
            player.get_texture().blit(pos1,pos2, width=dim1, height=dim2)
            
    def close(event):
        player.delete()
        window.close()
        source.delete()
        pyglet.app.exit()
    
    pyglet.clock.schedule_once(close,stopper)
    pyglet.app.run()
    stop=time.time() #timestemp of stop
    stopper_manager.value=2
    
    '''closing video'''
    window.close(), player.delete(), source.delete(),pyglet.app.exit()
    log.append('Webcam stoppped'+' : '+str(stop))
    log.append('Video start'+' : '+str(start))
    log.append('Video stop'+' : '+str(stop))
    process2.join() #waiting for the closing of process2
    
    # =============================================================================
    # BYBY
    # =============================================================================
    if num =='0':
        byby='\nThe first session is now finished.\n    Remeber to watch the second video tomorrow.    \n\n    Thank you for your participation!    \n'
    elif num=='1':
        byby='\nThe second session is now finished.\n    Remeber to watch the third video tomorrow.    \n\n    Thank you for your participation!    \n'
    elif num=='2':
        byby='\nYou completed all three sessions.\n    Remember your appointment for the EEG session.    \n\n    Thank you for your participation!    \n'
    
    window = tkinter.Tk()
    window.title("Goodbye")
    tkinter.Label(window, text=byby,font=("Arial Bold", int(screen_w/96)),anchor='center').pack()
    btn = tkinter.Button(window, text="Goodbye",font=("Arial Bold", int(screen_w/96)), command=window.destroy, anchor='s').pack()
    center(window)  #definition that take in account everything and center the window
    window.mainloop()
    sys.exit()