# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 11:50:23 2020

@author: Tommaso
"""
from threading import Thread

import PIL.Image
import cv2
import multiprocessing
import pyglet
import time
import os


class WEBCAM:
    """Class to record the webcam in parallel to the stimuli presentation"""

    def __init__(self, activator, fps_in):
        self.fps = int(fps_in.value * 0.8)  # reducing of 20% the framerate
        self.TIMEOUT = 1 / self.fps  # convert to milliseconds for the timeout
        self.activator = activator

        self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)  # finding the webcam
        self.ret, self.OUT = self.cap.read()  # reading one frame to extract details

        self.width = 320  # width of the frame that will be saved
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * self.width / self.cap.get(
            cv2.CAP_PROP_FRAME_WIDTH))  # height related to width
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # CODEC
        self.out = cv2.VideoWriter(os.path.dirname(os.path.realpath(__file__)) + "\\output.mp4",
                                   self.fourcc, self.fps, (self.width, self.height))  # Saving details

        self.activation = True
        self.capturing = Thread(target=self.capture, args=())  # threading webcam frame reading

        # initiate
        self.begin()

    def begin(self):
        self.capturing.start()
        old_timestamp = time.time()
        while True:
            if self.activator.value > 1:
                if (time.time() - old_timestamp) > self.TIMEOUT:  # waiting loop
                    self.out.write(self.OUT)
                    old_timestamp = time.time()

            elif self.activator.value == 0:  # while 0 do not save frames
                continue
            elif self.activator.value == 1:  # Stop saving
                self.activation = False
                self.cap.release()
                self.out.release()
                break
        return ()

    def capture(self):
        # Threaded reading of frames. This allows to have always a frame to save

        while self.activation == True:
            ret, frame = self.cap.read()
            self.OUT = cv2.resize(cv2.flip(frame, 1), (self.width, self.height),
                                  interpolation=cv2.INTER_NEAREST)  # saving frame
        return ()


class Webcam_feedback(pyglet.window.Window):
    """Function to see a feedback from the webcam
    This can be used frame better the subject or object"""

    def __init__(self):
        super(Webcam_feedback, self).__init__(vsync=True, style="borderless")

        self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)  # finding the webcam
        time.sleep(0.2)
        ret, self.frame = self.cap.read()  # reading the frames
        self.cv2glet()

        # Pyglet window setting
        w = pyglet.canvas.get_display().get_screens()[0].width  # screen dimension width
        self.set_size(self.pyimg.width, self.pyimg.height)
        self.set_location(int(w / 2 - self.pyimg.width / 2), 0)  # set location of the window
        pyglet.clock.schedule_interval(self.update, 0.01)  # update interval

    def update(self, dt):
        return ()

    def on_draw(self):
        self.clear()
        ret, self.frame = self.cap.read()
        self.cv2glet()  # conversion of the frames
        self.pyimg.blit(0, 0)

    def cv2glet(self):
        self.to_convert = cv2.flip(self.frame, 1)  # flipping the frame

        # Assumes image is in BGR color space. Returns a pyimg object
        rows, cols, channels = self.to_convert.shape
        raw_img = PIL.Image.fromarray(self.to_convert).tobytes()

        top_to_bottom_flag = -1
        bytes_per_row = channels * cols
        self.pyimg = pyglet.image.ImageData(width=cols, height=rows, format="BGR", data=raw_img,
                                            pitch=top_to_bottom_flag * bytes_per_row)
        return self.pyimg

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:  # removing functionality of ESC
            return True
        elif symbol == pyglet.window.key.SPACE:  # Spacebar close the process
            self.cap.release()
            return self.close()


def fps_checker(manager_of_frames):
    """Function to check the framerate of teh webcam"""

    manager_of_frames.value = 0  # make sure we start from 0
    fps_testing = 0
    check = cv2.VideoCapture(0 + cv2.CAP_DSHOW)  # finding the webcam

    if not check.isOpened():
        manager_of_frames.value = 1  # if the webcam is not opened by VideoCapture set the manager to 1 as error code
        print("Webcam cannot be found")

    else:
        start_testing = time.time()
        while fps_testing < 200:  # read 200 frames anc use the time to find the framerate
            ret, frame = check.read()
            frame = cv2.flip(frame, 1)
            fps_testing = fps_testing + 1
        stop_testing = time.time()

        manager_of_frames.value = round(fps_testing / (stop_testing - start_testing))
        print(str(manager_of_frames.value))
        check.release()
        print("Webcam identified and fps extracted")
    return ()


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()

    pyglet.media.have_ffmpeg()
    # =============================================================================
    # Multiprocessing setting
    # =============================================================================
    fps_manager = manager.Value("i", 0)
    activator_manager = manager.Value("i", 0)

    process1 = multiprocessing.Process(target=fps_checker, args=(fps_manager,))
    process2 = multiprocessing.Process(target=WEBCAM, args=(activator_manager, fps_manager))

    # =============================================================================
    # The actual EXP 
    # =============================================================================

    # Screen dimension
    screen_w = pyglet.canvas.get_display().get_screens()[0].width
    screen_h = pyglet.canvas.get_display().get_screens()[0].height
    video_w, video_h = 1920, 1080
    rapport = screen_h/video_h
    pos1, pos2, dim1, dim2 = screen_w / 2 - video_w * rapport / 2, screen_h / 2 - video_h * rapport / 2, video_w * rapport, video_h * rapport

    #  Checking the framerate
    process1.start()
    process1.join()

    #  Feedback from the webcam to frame the subject
    Webcam_feedback()
    pyglet.app.run()

    # Start saving the videos in parallel process
    process2.start()  # start the process
    time.sleep(8)  # wait for everything to start up

    # Prepare the video
    window = pyglet.window.Window(fullscreen=True, vsync=True)
    vidPath = os.path.dirname(os.path.realpath(__file__)) + "\\video.mp4"
    player = pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    MediaLoad = pyglet.media.load(vidPath)
    player.queue(MediaLoad)
    player.play()

    activator_manager.value = 2  # starting to save the frames

    @window.event
    def on_draw():
        window.clear()
        if player.source and player.source.video_format:
            player.get_texture().blit(pos1, pos2, width=dim1, height=dim2)

    @window.event
    def on_close():
        player.delete()
        window.close()
        source.delete()
        pyglet.app.exit()

    @player.event
    def on_eos():
        player.delete()
        window.close()
        source.delete()
        pyglet.app.exit()

    pyglet.app.run()

    """closing video"""
    window.close(), pyglet.app.exit(), source.delete(), player.delete()

    activator_manager.value = 1  # starting to save the frames
    process2.join()
