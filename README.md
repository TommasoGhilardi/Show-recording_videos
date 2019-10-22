# Program to display a video while recording from the webcam.
The script was created for an EEG training experiment.
In this experiment infants had to watch 3 videos at home. The script was created to be tranformed in an executable for Windows and Mac using pyinstaller.

The program will look for "data" (where the webcam recordings will be stored) and "set" (where the videos to display are stored) folders.

The program utilize:
- pyglet to display the videos
- cv2 to collect the video from the webcam
- tkinter to display messages

The program requires [FFMPEG](https://www.ffmpeg.org/download.html)


Included the icon (both for Windows and Mac)

![smile](https://user-images.githubusercontent.com/38372956/66559387-9c631f00-eb55-11e9-8d79-547684e4226f.png)

