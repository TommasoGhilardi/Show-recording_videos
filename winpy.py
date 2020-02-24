# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:12:40 2019

@author: Tommaso Ghilardi
"""
import os , sys, cv2, time, PIL.Image
import pyglet, multiprocessing
from os import listdir

# =============================================================================
# Functions pyglet
# =============================================================================
def messages(disp_text,handler,stopper):
    
    # Handler 0: SPACE close the window and ESCAPE do nothing 
    # Handler 1: SPACE close the window and ESCAPE close the program
    # Handler 2: SPACE and ESCAPE do nothing (waiting for stopper seconds)
    # Handler 3: Press a button between 1 and 9
    
    w = pyglet.canvas.get_display().get_screens()[0].width
    h = pyglet.canvas.get_display().get_screens()[0].height

    batch = pyglet.graphics.Batch()
    
    document = pyglet.text.document.FormattedDocument()
    disp=pyglet.text.layout.TextLayout(document)
    
    Size_font=30
    
    while disp.content_height==0 or disp.content_height>=int(h*0.75):

        Size_font=Size_font-2 
        document = pyglet.text.document.FormattedDocument()
        batch = pyglet.graphics.Batch()

        document.insert_text(0, disp_text, attributes=dict(font_name='Times New Roman', font_size=Size_font, align='center',
                                                              margin_top=Size_font*0.8, margin_bottom=Size_font*0.8, 
                                                              margin_right=Size_font*0.6, margin_left=Size_font*0.6,
                                                              line_spacing=Size_font*0.8, leading=Size_font*0.5,
                                                              wrap=True, color=(255, 255, 255, 255)))
        disp=pyglet.text.layout.TextLayout(document, width=int(w*0.8), height=int(h*0.75),
                                               multiline=True, wrap_lines='yes', batch=batch)

    window = pyglet.window.Window(int(w*0.8),int(h*0.75),resizable=False,visible = True,style='borderless' )
    window.set_location(int(w/2-int(w*0.8)/2),100)
    
    def update(dt):
        return()  
    pyglet.clock.schedule_interval(update, 0.01)
    
    @window.event
    def on_draw():
        window.clear()
        batch.draw()
    
    @window.event
    def on_key_press(symbol,modifier):
        if handler==0:
            if symbol==pyglet.window.key.ESCAPE:
                return True
            elif symbol==pyglet.window.key.SPACE:
                return window.close()
        elif handler==1:
            if symbol==pyglet.window.key.ESCAPE:
                return sys.exit()
            elif symbol==pyglet.window.key.SPACE:
                return window.close()
        elif handler==2:
            if symbol==pyglet.window.key.ESCAPE:
                return True
            elif symbol==pyglet.window.key.SPACE:
                return True
        elif handler ==3:
            print(pyglet.window.key.symbol_string(symbol))
            if pyglet.window.key.symbol_string(symbol)[-1].isdigit():
                if 1<=int(pyglet.window.key.symbol_string(symbol)[-1])<=9:
                    global rating
                    rating=pyglet.window.key.symbol_string(symbol)[-1]
                    window.close()
            
    def closx(event):
        window.close()
        pyglet.app.exit()
    
    if handler==2:
        pyglet.clock.schedule_once(closx,stopper)

    pyglet.app.run()
    return()
    
# =============================================================================
# Functions webcam    
# =============================================================================
def Webcam_feedback():
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    ret,frame=cap.read()
    
    def cv2glet(img):
        '''Assumes image is in BGR color space. Returns a pyimg object'''
        rows, cols, channels = img.shape
        raw_img = PIL.Image.fromarray(img).tobytes()
        
        top_to_bottom_flag = -1
        bytes_per_row = channels*cols
        pyimg = pyglet.image.ImageData(width=cols, height=rows, format='BGR', data=raw_img, 
                                       pitch=top_to_bottom_flag*bytes_per_row)
        return(pyimg)
    
    pimg=cv2glet(frame)
    
    def update(dt):
        return()
    
    """screen dimension"""
    w = pyglet.canvas.get_display().get_screens()[0].width
    
    window=pyglet.window.Window(pimg.width,pimg.height, vsync= True,style='borderless')
    window.set_location(int(w/2-pimg.width/2),0)
    pyglet.clock.schedule_interval(update, 0.01)
       
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol==pyglet.window.key.ESCAPE:
            return True
        elif symbol==pyglet.window.key.SPACE:
            return window.close()

    @window.event
    def on_draw():
        window.clear()
        ret,frame=cap.read()
        pimg=cv2glet(cv2.flip(frame,1))
        pimg.blit(0,0)
        
    pyglet.app.run()
    cap.release()
    return()    
    
def check_webcam(manager_of_frames,path,numm):
    manager_of_frames.value=0
    fps_testing=0
    check = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    
    if not check.isOpened():
        manager_of_frames.value=1

    else:
        width_w= 320
        height_w= int(check.get(cv2.CAP_PROP_FRAME_HEIGHT)*width_w/check.get(cv2.CAP_PROP_FRAME_WIDTH))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")#'DIVX', *'mp4v', *'X264',  [mp4 +'avc1'] [avi + 'DIVX']
        out = cv2.VideoWriter(path+'\\data\\try.mp4',fourcc,20,(width_w,height_w))
        out.set(cv2.VIDEOWRITER_PROP_QUALITY,50)
        
        start_testing=time.time()
        while fps_testing<150:
            ret, frame = check.read()
            frame=cv2.resize(frame,(width_w,height_w),interpolation=cv2.INTER_NEAREST)
            if ret == True:
                out.write(frame)
                fps_testing= fps_testing+1
        stop_testing=time.time()
        
        manager_of_frames.value=round(fps_testing/(stop_testing-start_testing))
        print(str(manager_of_frames.value))
        check.release()
        out.release()
        print('Webcam identified')
        os.remove(path+'\\data\\try.mp4')
    return()

def webcam(stopper,fps,path,numm):
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    # Timeout to display frames in seconds FPS = 1/TIMEOUT 
    print(fps.value)
    if fps.value >20:
        fps_out =15
    if 15< fps.value <=20:    
        fps_out = 10            #15 fps
    elif 10< fps.value <=15:
        fps_out = 8             #10 fps
    elif fps.value <= 10:
        fps_out = 5             #5 fps
    TIMEOUT= 1/fps_out
    
    """Saving video settings"""
    width_w= 320
    height_w= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*width_w/cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")#'DIVX', *'mp4v', *'X264',  [mp4 +'avc1'] [avi + 'DIVX']
    out = cv2.VideoWriter(path+'\\data\\webcam_'+numm+'.mp4',fourcc,fps_out,(width_w,height_w),isColor=True)
    out.set(cv2.VIDEOWRITER_PROP_QUALITY,80)
    
    old_timestamp = time.time()
    
    while True:
        if stopper.value > 1:
            if (time.time() - old_timestamp) > TIMEOUT:
                ret, frame = cap.read()
                frame=cv2.resize(frame,(width_w,height_w),interpolation=cv2.INTER_NEAREST)
                out.write(frame)
                old_timestamp = time.time()
            
        elif stopper.value==0:
            continue
        elif stopper.value==1:    
            cap.release()
            out.release()
            break
    return()     

# =============================================================================
# General funcitons    
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
        Video0,Video1,Video2 =pathh+'\\'+'video0.mp4',pathh+'\\'+'video1.mp4',pathh+'\\'+'video2.mp4'
        print('Videos identified')
        log.append('Video identified'+' : '+str(time.time()))
    else:
        problem= 'The program is unable to detect the media files.\n\n\
        If you have modified or moved any file on the USB drive, please restore the original state of the USB drive.\n\
        If unable to restore the original state, please contact the researcher by following the provided instruction.\n'
        messages(problem,2,8)
        sys.exit()
    return(Video0,Video1,Video2)
   
def exit_all():
    sys.exit()
    window.destroy()

# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    # pyglet.options['search_local_libs'] = True
    print('The system has FFMEPG = ' + str(pyglet.media.have_ffmpeg()))

    # =============================================================================
    # Waiting window + screen realted info
    # =============================================================================
    log=list() #logfile to store informations
    rating= 'null' #rating of the infant attention
    
    screen_w = pyglet.canvas.get_display().get_screens()[0].width
    screen_h= pyglet.canvas.get_display().get_screens()[0].height
    
    excuses='\n\nWelcome and thank you for participating in this study'
    messages(excuses,2,3)
    
    # Get time and date
    log.append('Video watched on'+' : '+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    
    video_w, video_h=1440,1080
    rapport = screen_h/video_h
        
    # =============================================================================
    # Main
    # =============================================================================
    final = find_folder() #find the folder where the script is in    
    SET = [s for s in listdir(final) if 'set' in s][0]
    log.insert(0,'The training set is: '+SET+'\n')
    video0,video1,video2= findinpath(final+'\\'+SET)  #selecting the videos in the folders

    # =============================================================================
    # Check which video to show(which session we are)
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
        thanks='\n\nIt seems that you have already partecipated to all three sessions\n\n\
            Thank for your time!!'+'\n'
        messages(thanks,2,6)
        sys.exit()
    
    log.append('Identified session'+' : '+str(time.time()))
    print('Identified session')

    # =============================================================================
    # Multiprocessing setting
    # =============================================================================
    fps_manager = manager.Value('i', 0)
    stopper_manager = manager.Value('i',0)
    
    process1 = multiprocessing.Process(target=check_webcam, args=(fps_manager,final,num)) 
    process2 = multiprocessing.Process(target=webcam, args=(stopper_manager,fps_manager,final,num)) 

    # =============================================================================
    # Welcome window
    # =============================================================================
    process1.start()
    time.sleep(1)
    instructions= '\nThank you for participating in this study.\n This study is divided into two phases: the training phase and the testing phase.\n\n \
    The training phase will take place during the three days before the test phase.\n \
    During this period we ask you to watch three videos (one each day) using this program.\n \
    In each session a video will be displayed on your screen, while a feedback from the webcam will be recorded.\n\n\
    The program will not install anything on your device and the videos will only be saved on the encrypted USB drive:   \n\
    you will have complete control over them.\n\n\
    Please remember to bring the USB drive to the test phase.\n\
    The videos will be analyzed in order to evaluate the level of attention paid to the stimuli.\n\n \
    When you are ready, press the SPACEBAR to progress with the session.\n'
    messages(instructions,1,0)

    # =============================================================================
    # Waiting for the framerate 
    # =============================================================================
    waiting = '\n\nThe program is checking the framerate of your webcam.\n\n\
        Please wait.'
    messages(waiting,2,5)

    process1.join()
    
    # =============================================================================
    # Problem webcam
    # =============================================================================
    if fps_manager.value==1:
        problem='The program is unable to detect a webcam.\n\
        Please make sure that your computer or device has access to a webcam and try to start the program again.'
        messages(problem,2,4)
        sys.exit()
    
    log.append('Webcam identification'+' : '+str(time.time())) 
    log.append('Framerate of'+' : '+str(fps_manager.value)+' fps')
    
   # =============================================================================
    # Ready window
    # =============================================================================
    position='\nPressing the SPACEBAR will display a video feedback from your webcam.\n\
    Try to position yourself in front of the webcam in order  to frame your face as accurately as possible.\n\
    When satisfied with the framing plese press the SPACEBAR to continue.'
    messages(position,0,0)
    Webcam_feedback()
    print('Image checked on webcam')
    log.append('Image checked on webcam'+' : '+str(time.time())) 

    # =============================================================================
    # Last Chance
    # =============================================================================
    readyness='\nPressing the SPACEBAR will start the video session.\n\
    The session will last around 12 minutes.\n\n\
    If you are not ready or you prefer to start the session later,\n please click ESCAPE and the program will close.\n\n\
    If you decide to proceed please click the SPACEBAR button. We ask you to try to watch the entire session.   \n\n\
    If for any reason you decide to interrupt the session please press the ESC key.'
    messages(readyness,1,0)
    print('Session accepted')
    log.append('Session accepted'+' : '+str(time.time()))

    # =============================================================================
    #  showing video
    # =============================================================================
    process2.start()
    print('Webcam activated')
    log.append('Webcam activated'+' : '+str(time.time()))
    time.sleep(1)
        
    pos1,pos2,dim1,dim2=screen_w/2-video_w*rapport/2, screen_h/2-video_h*rapport/2 ,video_w*rapport,video_h*rapport
    window=pyglet.window.Window(fullscreen=True, vsync= True)
    player=pyglet.media.Player()
    source = pyglet.media.load(showing)
    source.video_format.frame_rate=15
    player.queue(source)
    player.play()
    stopper_manager.value=2
    start=time.time() #timestemp of start
    
    @window.event
    def on_draw():
        window.clear()
        if player.source and player.source.video_format:
            player.get_texture().blit(pos1,pos2, width=dim1, height=dim2)
            
    @window.event
    def on_close():
        player.delete()
        window.close()
        source.delete()
        pyglet.app.exit()
        print('close')
        
    @player.event
    def on_eos():
        player.delete()
        window.close()
        source.delete()
        pyglet.app.exit()
        print('eos')
        
    pyglet.app.run()
    stop=time.time() #timestemp of stop
    stopper_manager.value=1
    
    '''closing video'''
    window.close(), player.delete(), source.delete(),pyglet.app.exit()
    log.append('Video start : '+str(start))
    log.append('Video stop : '+str(stop))
    minutes,seconds=divmod(stop-start,60)
    log.append('Duration : '+str(int(minutes))+':'+str(seconds))
    process2.join() #waiting for the closing of process2
    
    # =============================================================================
    # Rating Infant  
    # =============================================================================
    rating_text='\nPlease rate the attention of the child to the video.\n\n\
        Press a numeric button between 1 and 9 where:\n\n\
            1 means the infant paid no attention to the video\n\
                9 means the infant paid attettion to the whole video'
    messages(rating_text,3,0)
    log.append('Infant attention rated as : '+rating)
    print(rating)
    
    # =============================================================================
    # saving logs
    # =============================================================================
    logg= open(final+'\\data\\log_'+num+'.txt','w+')
    for err in log:
        logg.write(err+'\n') 
    logg.close() 
    time.sleep(1)
    
    # =============================================================================
    # BYBY
    # =============================================================================
    if num =='0':
        byby='\n\nThe first session is now finished.\n    Please remeber to watch the second video tomorrow.    \n\n    Thank you for your participation!    \n'
    elif num=='1':
        byby='\n\nThe second session is now finished.\n    Please remeber to watch the third video tomorrow.    \n\n    Thank you for your participation!    \n'
    elif num=='2':
        byby='\n\nYou completed all three sessions.\n    Please remember your appointment for the EEG session.    \n\n    Thank you for your participation!    \n'
    
    messages(byby,2,4)
    sys.exit()